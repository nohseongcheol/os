"""Execute the freestanding library's boundary tests as a Linux i386 test ELF.

Guest ELFs use a custom non-page-aligned WorldOS linker layout; the host test is
linked separately with Linux-compatible ELF segments, not run from guest build/.
"""
from pathlib import Path
import subprocess
import tempfile
import unittest

from install_posix import canonical_sources
from posix_terms import FUNCTION_KEYS, LOCAL_KEYS, explicit
from posix_library_terms import FUNCTION_KEYS as LIBRARY_FUNCTION_KEYS
from native_source import inverse, local_path
from install_shells import assign
from posix_build import c_transform


class PosixLibraryTests(unittest.TestCase):
    def test_localized_library_roundtrip(self):
        repository = Path(__file__).resolve().parents[1]
        for language in ('ko', 'ja', 'ja_Hira', 'ja_Kana', 'zh_Hans', 'zh_Hant'):
            values, _ = explicit(language)
            self.assertTrue(set(LIBRARY_FUNCTION_KEYS).issubset(values))
            names = assign(set(FUNCTION_KEYS + LOCAL_KEYS), values)
            for source in (repository / 'tools/posix_library').rglob('*'):
                if source.suffix not in ('.c', '.h'):
                    continue
                text = source.read_text(encoding='utf-8')
                self.assertEqual(c_transform(c_transform(text, names), inverse(names)), text)

    def test_host_i386_library_boundaries(self):
        self.host_test(False)

    def test_allocator_growth_failure_alignment_and_coalescing(self):
        self.host_test(True)

    def host_test(self, fault_injection):
        repository = Path(__file__).resolve().parents[1]
        sources, _ = canonical_sources(local_path(repository / '나라/KOR', '소스'))
        selected = {name: data for name, data in sources.items() if name.startswith('include/') or
                    name in ('src/crt0.S', 'src/syscall.S', 'src/errno.c', 'src/unistd.c', 'src/stat.c')}
        for path in (repository / 'tools/posix_library').rglob('*'):
            if path.is_file():
                selected[str(path.relative_to(repository / 'tools/posix_library'))] = path.read_bytes()
        if fault_injection:
            del selected['tests/library.c']
            selected['tests/library_main.c'] = (repository / 'tools/posix_allocation_fault_test.c').read_bytes()
        with tempfile.TemporaryDirectory(prefix='worldos-posix-library-test-') as temporary:
            root = Path(temporary)
            objects = []
            for relative, data in selected.items():
                path = root / relative
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_bytes(data)
            for path in sorted(root.rglob('*')):
                if path.suffix not in ('.c', '.S'):
                    continue
                output = root / (path.stem + '.o')
                extra = ['-Dsbrk=allocation_test_sbrk'] if fault_injection and path.name == 'allocation.c' else []
                subprocess.check_output(['gcc', '-m32', '-ffreestanding', '-fno-builtin', '-fno-pie',
                    '-fno-pic', '-fno-stack-protector', '-Wall', '-Wextra', '-Werror', '-nostdinc',
                    '-I' + str(root / 'include'), '-c', str(path), '-o', str(output)] + extra, stderr=subprocess.STDOUT)
                objects.append(str(output))
            executable = root / 'library-test'
            subprocess.check_output(['ld', '-m', 'elf_i386', '-static', '-e', '_start', '-o', str(executable)] + objects, stderr=subprocess.STDOUT)
            result = subprocess.check_output([str(executable)], stderr=subprocess.STDOUT, timeout=20)
            self.assertEqual(result, b'POSIX-ALLOCATOR:PASS\n' if fault_injection else b'POSIX-LIBRARY:PASS\n')


if __name__ == '__main__':
    unittest.main()
