import importlib.util
import io
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tarfile
import tempfile
import unittest
from unittest import mock

HERE = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location('portable_release', str(HERE / 'portable.py'))
portable = importlib.util.module_from_spec(spec); spec.loader.exec_module(portable)


class PortableTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory(prefix='portable test ')
        self.addCleanup(self.temporary.cleanup)
        self.base = Path(self.temporary.name)
        self.root = self.base / 'original source'
        (self.root / 'distribution').mkdir(parents=True)
        shutil.copy2(str(HERE / 'portable.py'), str(self.root / 'distribution/portable.py'))
        shutil.copy2(str(HERE.parent / 'unpack.sh'), str(self.root / 'unpack.sh'))
        (self.root / 'source.java').write_text('keep this source')
        (self.root / 'build').mkdir(); (self.root / 'build/user.img').write_text('private disk')
        (self.root / '.vbox').mkdir(); (self.root / '.vbox/state').write_text('private VM')
        (self.root / 'vendor').mkdir()
        self.upstream = self.base / 'upstream.bin'; self.upstream.write_bytes(b'upstream dependency')
        shutil.copy2(str(self.upstream), str(self.root / 'vendor/dependency.bin'))
        self.dependency = {'url': self.upstream.as_uri(), 'sha256': portable.sha(self.upstream),
                           'files': [{'path': 'vendor/dependency.bin', 'sha256': portable.sha(self.upstream)}]}
        self.cfg = {'project': 'jkoros', 'downloads': [self.dependency]}
        (self.root / 'distribution/dependencies.json').write_text(json.dumps(self.cfg))
        self.archive = self.base / 'release/source.tar.gz'

    def package(self):
        portable.pack(self.root, self.archive, 0)

    def test_default_pack_creates_real_gzip_archive(self):
        with mock.patch.object(sys, 'argv', ['portable.py', 'pack', '--root', str(self.root)]):
            portable.main()
        archive = self.root / 'dist/jkoros-source.tar.gz'
        self.assertEqual(archive.read_bytes()[:2], b'\x1f\x8b')
        with tarfile.open(str(archive), 'r:gz') as stream:
            self.assertEqual(stream.extractfile('source.java').read(), b'keep this source')

    def test_pack_rejects_misleading_xz_filename(self):
        archive = self.base / 'release/source.tar.xz'
        with self.assertRaisesRegex(ValueError, 'must end with .tar.gz'):
            portable.pack(self.root, archive)
        self.assertFalse(archive.exists())

    def test_standalone_unpack_handles_gzip_and_legacy_xz(self):
        self.package()
        legacy = self.base / 'legacy.tar.xz'
        with tarfile.open(str(self.archive), 'r:gz') as source, tarfile.open(str(legacy), 'w:xz') as target:
            for member in source:
                target.addfile(member, source.extractfile(member) if member.isfile() else None)
        for number, archive in enumerate((self.archive, legacy)):
            destination = self.base / ('restored project ' + str(number))
            subprocess.check_output(['sh', str(self.archive.parent / 'unpack.sh'), str(archive),
                                     str(destination), '--no-prepare'], stderr=subprocess.STDOUT)
            self.assertEqual((destination / 'source.java').read_text(), 'keep this source')

    def test_excludes_without_deleting_and_restores_downloads(self):
        self.package()
        self.assertTrue((self.root / 'build/user.img').is_file())
        self.assertEqual((self.root / 'vendor/dependency.bin').read_bytes(), self.upstream.read_bytes())
        target = portable.unpack(self.archive, self.base / 'relocated project')
        self.assertFalse((target / 'build').exists())
        self.assertFalse((target / '.vbox').exists())
        self.assertFalse((target / 'vendor/dependency.bin').exists())
        state = json.loads((target / portable.STATE).read_text())
        portable.restore_downloads(target, state['downloads'], 'all')
        self.assertEqual((target / 'vendor/dependency.bin').read_bytes(), self.upstream.read_bytes())
        self.assertEqual((target / 'source.java').read_text(), 'keep this source')

    def test_modified_vendor_file_is_included(self):
        (self.root / 'vendor/dependency.bin').write_bytes(b'local change')
        self.package(); target = portable.unpack(self.archive, self.base / 'restored')
        state = json.loads((target / portable.STATE).read_text())
        self.assertEqual(state['downloads'], [])
        self.assertEqual((target / 'vendor/dependency.bin').read_bytes(), b'local change')

    def test_relative_links_survive_moving(self):
        (self.root / 'link').symlink_to('source.java')
        self.package(); target = portable.unpack(self.archive, self.base / 'restored')
        moved = self.base / 'moved'; target.rename(moved)
        self.assertEqual((moved / 'link').read_text(), 'keep this source')

    def test_download_mismatch_never_installs_partial_file(self):
        target = self.base / 'restored'; target.mkdir()
        self.upstream.write_bytes(b'wrong bytes')
        with mock.patch.object(portable.time, 'sleep'):
            with self.assertRaisesRegex(ValueError, 'checksum mismatch'):
                portable.restore_downloads(target, [self.dependency], 'all')
        self.assertFalse((target / 'vendor/dependency.bin').exists())

    def test_archive_checksum_failure_keeps_destination_absent(self):
        self.package()
        with self.archive.open('ab') as stream: stream.write(b'tamper')
        target = self.base / 'restored'
        with self.assertRaisesRegex(ValueError, 'checksum mismatch'):
            portable.unpack(self.archive, target)
        self.assertFalse(target.exists())

    def test_existing_destination_is_not_overwritten(self):
        self.package()
        with self.assertRaisesRegex(ValueError, 'already exists'):
            portable.unpack(self.archive, self.root)
        self.assertEqual((self.root / 'source.java').read_text(), 'keep this source')

    def test_traversal_is_rejected(self):
        archive = self.base / 'unsafe.tar.gz'
        with tarfile.open(str(archive), 'w:gz') as stream:
            entry = tarfile.TarInfo('../outside'); entry.size = 1
            stream.addfile(entry, io.BytesIO(b'x'))
        with self.assertRaisesRegex(ValueError, 'Unsafe package path'):
            portable.unpack(archive, self.base / 'restored')
        self.assertFalse((self.base / 'outside').exists())

    def test_external_source_symlink_is_not_packed(self):
        (self.root / 'outside').symlink_to(self.upstream)
        with self.assertRaisesRegex(ValueError, 'external symlink'):
            self.package()
        self.assertFalse(self.archive.exists())

    def test_unpack_defaults_to_automatic_preparation(self):
        root = self.base / 'restored'
        with mock.patch.object(sys, 'argv', ['portable.py', 'unpack', 'input.tar.gz', str(root)]), \
             mock.patch.object(portable, 'unpack', return_value=root), \
             mock.patch.object(portable.subprocess, 'check_call') as run:
            portable.main()
        self.assertEqual(run.call_args[0][0], [sys.executable, str(root / 'distribution/portable.py'),
                                              'prepare', '--profile', 'all'])


if __name__ == '__main__':
    unittest.main()
