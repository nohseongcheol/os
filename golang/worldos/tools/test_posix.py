import json
from pathlib import Path
import shutil
import tempfile
import unittest
from unittest.mock import patch

from install_shells import assign
from install_posix import language_code, terminology, canonical_sources, install, package_directory, addition
from migrate_posix_country import migrate
from generate_script_variants import rows as table_rows
from neutralize_posix import neutral
from native_source import inverse, safe, local_path
from posix_build import c_transform, lower, verify, digest
from posix_terms import explicit, FUNCTION_KEYS, LOCAL_KEYS, FUNCTION_ROWS
from variant_terms import INDIA
from summarize_posix import apply_retry


class PosixTests(unittest.TestCase):
    def test_rows_and_identifier_roundtrip(self):
        keys = set(FUNCTION_KEYS + LOCAL_KEYS)
        for language in list(FUNCTION_ROWS) + ['ja_Hira', 'ja_Kana', 'en', 'ta_Taml']:
            with self.subTest(language=language):
                values, _, _ = terminology(Path('/nonexistent'), language)
                names = assign(keys, values)
                source = ' '.join(sorted(keys))
                self.assertEqual(c_transform(c_transform(source, names), inverse(names)), source)

    def test_korean_current_semantics(self):
        values, _ = explicit('ko')
        self.assertEqual(values['read'], '읽기')
        self.assertEqual(values['write'], '쓰기')
        self.assertIn('참조복제', values['dup'])
        self.assertIn('실행내용바꾸기', values['execve'])
        self.assertEqual(set(FUNCTION_KEYS + LOCAL_KEYS) - set(values), set())

    def test_japanese_scripts_and_readings(self):
        for language, low, high in [('ja_Hira', 0x3040, 0x309f), ('ja_Kana', 0x30a0, 0x30ff)]:
            names, paths = explicit(language)
            for value in list(names.values()) + list(paths.values()):
                self.assertTrue(all(low <= ord(ch) <= high or ch.isdigit() for ch in value), value)
        self.assertEqual(explicit('ja_Hira')[0]['argv'], 'ひきすういちらん')
        self.assertEqual(explicit('ja_Kana')[0]['read'], 'ヨム')

    def test_all_indian_primary_profiles_have_read_write(self):
        for alpha2, _, _, script in INDIA:
            names, _, _ = terminology(Path('/nonexistent'), alpha2 + '_' + script)
            self.assertIn('read', names, alpha2)
            self.assertIn('write', names, alpha2)
        self.assertNotEqual(terminology(Path('/nonexistent'), 'ta_Taml')[0]['read'], terminology(Path('/nonexistent'), 'hi_Deva')[0]['read'])

    def test_unknown_language_does_not_claim_translation(self):
        names, _, status = terminology(Path('/nonexistent'), 'und')
        self.assertFalse(names)
        self.assertFalse(status)

    def test_language_codes(self):
        self.assertEqual(language_code('ko'), 'kor')
        self.assertEqual(language_code('ja_Hira'), 'jpn')
        self.assertEqual(language_code('ta_Taml'), 'tam')
        self.assertEqual(language_code('mni_Mtei'), 'mni')

    def test_country_package_directory(self):
        self.assertEqual(package_directory('KOR'), 'posix-KOR')
        self.assertEqual(package_directory('USA'), 'posix-USA')
        self.assertEqual(package_directory('IND/ta_Taml'), 'posix-IND')
        with self.assertRaises(ValueError):
            package_directory('../KOR')

    def test_retry_evidence_requires_unchanged_artifacts(self):
        original = {'edition': 'KOR', 'case': 'native', 'result': 'FAIL',
                    'program_sha256': 'program', 'kernel_iso_sha256': 'kernel'}
        retry = dict(original, result='PASS')
        self.assertEqual(apply_retry([original], [retry])[0]['result'], 'PASS')
        self.assertEqual(original['result'], 'FAIL')
        with self.assertRaises(RuntimeError):
            apply_retry([original], [dict(retry, program_sha256='different')])
        with self.assertRaises(RuntimeError):
            apply_retry([original], [dict(retry, kernel_iso_sha256='different')])
        with self.assertRaises(RuntimeError):
            apply_retry([original], [dict(retry, case='unknown')])
        with self.assertRaises(RuntimeError):
            apply_retry([original], [retry, retry])

    def test_headers_are_not_identifiers(self):
        source = '#include <sys/stat.h>\n#include "read.h"\nint read(int count);\n'
        names = {'read': '읽기', 'stat': '상태', 'count': '수'}
        includes = {'sys/stat.h': 'sys/자료상태.h', 'read.h': '자료읽기.h'}
        result = c_transform(source, names, includes)
        self.assertIn('<sys/자료상태.h>', result)
        self.assertIn('"자료읽기.h"', result)
        self.assertEqual(c_transform(result, inverse(names), inverse(includes)), source)
        self.assertIn('<sys/stat.h>', c_transform(source, names))

    def test_literal_comment_and_integer_suffix_preservation(self):
        source = '/* read U */ read(1UL, "read", 0xffU); // read\n'
        self.assertEqual(c_transform(source, {'read': '읽기', 'U': '접미', 'UL': '접미둘'}),
                         '/* read U */ 읽기(1UL, "read", 0xffU); // read\n')

    def test_combining_marks(self):
        names = {'read': 'पढ़ना', 'write': 'எழுது'}
        source = 'read(1); write(2);'
        self.assertEqual(c_transform(c_transform(source, names), inverse(names)), source)

    def test_neutral_names_are_idempotent_and_preserve_other_identifiers(self):
        old = '__engos_syscall6 __engos_syscall_result libengos_posix.a engos/syscall.h _ENGOS_UNISTD_H'
        result = neutral(old)
        self.assertEqual(result, '__syscall6 __syscall_result libposix.a sys/syscall.h _LIBC_UNISTD_H')
        self.assertEqual(neutral(result), result)
        self.assertEqual(neutral('this_engos_related_user_name'), 'this_engos_related_user_name')

    def test_korean_makefile_restores_compiler_include_directory(self):
        root = Path(__file__).resolve().parents[1]
        sources, _ = canonical_sources(local_path(root / '나라/KOR', '소스'))
        self.assertIn(b'-Iinclude', sources['Makefile'])
        self.assertNotIn('머리파일'.encode(), sources['Makefile'])

    def test_variant_makefile_restores_compiler_include_directory(self):
        root = Path(__file__).resolve().parents[1]
        for edition in ('JPN/ja_Hira', 'IND/ta_Taml', 'CHN/zh_Hant'):
            sources, _ = canonical_sources(local_path(root / '문자판' / edition, '소스'))
            self.assertIn(b'-Iinclude\n', sources['Makefile'])

    def test_verify_rejects_edited_source(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            source = root / '원문.c'
            source.write_text('int 읽기(void);', encoding='utf-8')
            config = {'names': {'read': '읽기'}, 'includes': {}, 'hashes': {'원문.c': digest(source.read_bytes())},
                'files': [{'native': '원문.c', 'compiler': 'source.c', 'kind': 'c', 'compiler_sha256': digest(b'int read(void);')}]}
            self.assertEqual(verify(root, config), 1)
            source.write_text('user changes', encoding='utf-8')
            with self.assertRaises(RuntimeError):
                verify(root, config)

    def test_reject_ambiguous_mapping_and_unsafe_paths(self):
        with self.assertRaises(ValueError):
            inverse({'read': '이름', 'write': '이름'})
        with self.assertRaises(ValueError):
            safe(Path('/tmp'), '../data')

    def test_refresh_preserves_extra_files_and_refuses_user_edits(self):
        repository = Path(__file__).resolve().parents[1]
        original = local_path(repository / '나라/KOR', '소스')
        with tempfile.TemporaryDirectory(prefix='worldos-posix-test-') as temporary:
            root = Path(temporary)
            parent = root / 'ZZZ'
            tree = parent / '소스'
            tree.mkdir(parents=True)
            (parent / 'Makefile').write_text('all:\n\ttrue\n')
            (root / 'tools').mkdir()
            for name in ('posix_probe.c', 'posix_build.py', 'native_source.py'):
                shutil.copy2(str(repository / 'tools' / name), str(root / 'tools' / name))
            shutil.copytree(str(repository / 'tools/posix_library'), str(root / 'tools/posix_library'))
            shutil.copy2(str(local_path(original, '파일대응표.tsv')), str(tree / '파일대응표.tsv'))
            for canonical, relative in table_rows(local_path(original, '파일대응표.tsv'))[1:]:
                if canonical.startswith('userland/posix/'):
                    destination = safe(tree, relative)
                    destination.parent.mkdir(parents=True, exist_ok=True)
                    shutil.copy2(str(safe(original, relative)), str(destination))
            record = ('ZZZ', parent, 'ko')
            install(root, record)
            package = parent / 'posix-ZZZ'
            config = json.loads((package / 'posix.json').read_text(encoding='utf-8'))
            (package / 'user-notes.txt').write_text('keep this')
            original_mkdtemp = tempfile.mkdtemp
            def confined_mkdtemp(suffix=None, prefix=None, dir=None):
                return original_mkdtemp(suffix=suffix, prefix=prefix, dir=str(root))
            with patch('install_posix.tempfile.mkdtemp', side_effect=confined_mkdtemp):
                install(root, record, refresh=True)
            self.assertEqual((package / 'user-notes.txt').read_text(), 'keep this')
            # Country-code migration must preserve all files and roll back safely
            # on conflicts, rather than treating an old language code as country.
            old_package = parent / 'posix-kor'
            package.rename(old_package)
            (parent / 'posix-entry.json').write_text('{"directory":"posix-kor"}\n')
            (parent / 'Makefile').write_text('all:\n\ttrue\n' + addition('posix-kor'))
            package.mkdir()
            with self.assertRaises(RuntimeError):
                migrate(root, record)
            package.rmdir()  # Only this empty test-created collision directory.
            with patch('migrate_posix_country.tempfile.mkdtemp', side_effect=confined_mkdtemp):
                migrate(root, record)
            self.assertFalse(old_package.exists())
            self.assertEqual((package / 'user-notes.txt').read_text(), 'keep this')
            self.assertEqual(json.loads((parent / 'posix-entry.json').read_text())['directory'], 'posix-ZZZ')
            self.assertIsNone(migrate(root, record))
            entry = next(e for e in config['files'] if e['compiler'] == 'src/unistd.c')
            source = safe(package, entry['native'])
            source.write_text('user edit', encoding='utf-8')
            with self.assertRaises(RuntimeError):
                install(root, record, refresh=True)
            self.assertEqual(source.read_text(), 'user edit')


if __name__ == '__main__':
    unittest.main()
