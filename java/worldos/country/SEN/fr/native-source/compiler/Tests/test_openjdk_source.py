import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from openjdk_build import build, BuildError
from openjdk_probe import inspect_elf, inspect_jdk


class OpenJDKSourceTest(unittest.TestCase):
    def setUp(self):
        self.work = tempfile.TemporaryDirectory(prefix='openjdk-route-')
        self.addCleanup(self.work.cleanup)
        self.root = Path(self.work.name)
        self.source = self.root / 'source'
        self.boot = Path(shutil.which('javac')).resolve().parents[1]

    def fixture_source(self, code):
        for name in ('make/autoconf/version-numbers', 'src/hotspot/share/runtime/os.hpp',
                     'src/java.base/share/classes/java/lang/Object.java'):
            p = self.source / name; p.parent.mkdir(parents=True, exist_ok=True); p.write_text('fixture\n')
        (self.source / 'configure').write_text(code)

    def test_configuration_failure_never_claims_success(self):
        self.fixture_source('echo intentional configure failure\nexit 17\n')
        output = self.root / 'result'
        with self.assertRaises(BuildError):
            build(self.source, output, self.boot)
        report = json.loads((output / 'jkoros-openjdk-build.json').read_text())
        self.assertFalse(report['passed'])
        self.assertFalse(report['native_kernel_port_complete'])
        self.assertEqual(report['stage'], 'configure')
        self.assertIn('17', report['error'])
        self.assertIn('intentional', (output / 'driver-configure.log').read_text())

    def test_unmanaged_directory_is_preserved(self):
        self.fixture_source('exit 0\n')
        output = self.root / 'project'; output.mkdir()
        (output / 'important.txt').write_text('preserve me')
        with self.assertRaises(BuildError): build(self.source, output, self.boot)
        self.assertEqual((output / 'important.txt').read_text(), 'preserve me')
        self.assertFalse((output / 'driver-configure.log').exists())

    def test_native_target_rejected_before_configure(self):
        self.fixture_source('echo must not run\nexit 0\n')
        output = self.root / 'native'
        with self.assertRaises(BuildError):
            build(self.source, output, self.boot, target='aarch64-jkoros')
        self.assertFalse(output.exists())

    def test_incomplete_source_and_overlapping_directory_rejected(self):
        with self.assertRaises(BuildError): build(self.source, self.root / 'out', self.boot)
        self.fixture_source('exit 0\n')
        with self.assertRaises(BuildError): build(self.source, self.source / 'build', self.boot)

    def test_real_openjdk_cannot_pass_native_check(self):
        report = inspect_jdk(self.boot)
        self.assertFalse(report['executed'])
        self.assertFalse(report['direct_copy_runnable'])
        self.assertFalse(report['native_kernel_port_complete'])
        self.assertTrue(report['binaries']['java']['native_abi_blockers'])
        self.assertIn('mmap', report['observed_os_imports']['memory_mapping'])
        self.assertIn('pthread_create', report['observed_os_imports']['native_threads_tls'])
        out = self.root / 'inspection.json'
        result = subprocess.run([sys.executable, str(ROOT / 'openjdk_probe.py'), '--jdk', str(self.boot),
                                 '-o', str(out), '--require-native'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        self.assertEqual(result.returncode, 3, result.stderr)
        self.assertFalse(json.loads(out.read_text())['direct_copy_runnable'])

    def test_elf_truncation_is_rejected(self):
        p = self.root / 'bad.elf'; p.write_bytes(b'\x7fELF\x02\x01')
        with self.assertRaises(ValueError): inspect_elf(p)


if __name__ == '__main__': unittest.main()
