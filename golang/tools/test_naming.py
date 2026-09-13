import json
from pathlib import Path
import subprocess
import tempfile
import unittest

from naming_lexicon import lexicon, IDENTIFIERS, PACKAGES
from refine_country_names import identifier, path_substitution, phrase, safe_join, FIXED


class NamingTests(unittest.TestCase):
    def test_all_phrase_tables_have_identical_concepts(self):
        languages = lexicon()
        self.assertEqual(22, len(languages))
        self.assertEqual(50, len(languages['en']))
        for language, concepts in languages.items():
            self.assertEqual(set(languages['en']), set(concepts), language)
            for text in concepts.values():
                self.assertTrue(identifier(text))

    def test_pending_language_is_not_claimed_translated(self):
        text, status = phrase('pau', 'append')
        self.assertEqual('pending-language-review', status)
        self.assertEqual(lexicon()['en']['append'], text)

    def test_undefined_language_is_not_counted_as_native_english(self):
        self.assertEqual('undefined-language-English', phrase('und', 'append')[1])

    def test_distinct_traditional_and_simplified(self):
        self.assertNotEqual(phrase('zh_Hans', 'file_read'), phrase('zh_Hant', 'file_read'))

    def test_explicit_whole_phrase_order(self):
        self.assertEqual('末尾に追加', phrase('ja', 'append')[0])
        self.assertEqual('Datei_lesen', identifier(phrase('de', 'file_read')[0], True, 'M'))

    def test_uncased_go_export_marker(self):
        self.assertEqual('M파일읽기', identifier('파일읽기', True, 'M'))
        self.assertEqual('T画面要素', identifier('画面要素', True, 'T', True))
        self.assertEqual('I画面要素', identifier('画面要素', True, 'I', True))

    def test_no_lossy_script_conversion(self):
        with self.assertRaises(ValueError):
            identifier('पढ़ना')

    def test_actual_behaviour_over_misleading_original_name(self):
        self.assertEqual('toggle_bit', IDENTIFIERS['UnsetBit'][0])
        self.assertEqual('set_coordinates', IDENTIFIERS['ModelToScreen'][0])

    def test_protocol_package_identity_retained_in_concept(self):
        self.assertEqual('ipv4', PACKAGES['ipv4'])
        self.assertEqual('udp', PACKAGES['udp'])

    def test_path_replacement_has_boundaries_and_is_not_recursive(self):
        source = 'nasm -I asm/ asm/rt0.s go_asm.h -Iinclude build/syscall.o'
        output = path_substitution(source, {'asm/': 'boot/', 'asm/rt0.s': 'boot/start.s',
                                            '-Iinclude': '-Ideclarations', 'boot/': 'BAD/'})
        self.assertEqual('nasm -I boot/ boot/start.s go_asm.h -Ideclarations build/syscall.o', output)

    def test_documented_directory_prefix(self):
        self.assertEqual('-I./사용자영역/posix/머리파일', path_substitution('-I./userland/posix/include',
                         {'userland/posix': '사용자영역/posix', 'userland/posix/include': '사용자영역/posix/머리파일'}))

    def test_path_escape_rejected(self):
        with self.assertRaises(RuntimeError):
            safe_join(Path('/tmp/example'), '../../elsewhere')
        with self.assertRaises(RuntimeError):
            safe_join(Path('/tmp/example'), '/etc/passwd')

    def test_external_names_are_protected(self):
        self.assertTrue(set(('main', 'init', 'KKernelEntry', 'Pointer', 'Data', 'Len', 'Cap')) <= FIXED)

    def test_tokens_preserve_comments_literals_and_operations(self):
        with tempfile.TemporaryDirectory(prefix='worldos-token-test-') as temporary:
            directory = Path(temporary)
            binary = directory / 'tokens'
            subprocess.check_call(['go', 'build', '-o', str(binary), str(Path(__file__).with_name('naming_tokens.go'))])
            source = 'package p\nimport "old/path"\n// oldName remains in this comment\nvar oldName = "old/path oldName"\nfunc f() { oldName += "oldName" }\n'
            path = directory / 'sample.go'
            path.write_text(source, encoding='utf-8')
            result = subprocess.check_output([str(binary)], input=json.dumps({'Files': [str(path)],
                'Names': {'oldName': '새이름'}, 'Imports': {'old/path': '새/경로'}}).encode())
            result = json.loads(result.decode())
            self.assertEqual(2, result['Replacements'])
            self.assertIn('import "새/경로"', result['Source'])
            self.assertIn('// oldName remains in this comment', result['Source'])
            self.assertIn('var 새이름 = "old/path oldName"', result['Source'])
            self.assertIn('새이름 += "oldName"', result['Source'])


if __name__ == '__main__':
    unittest.main()
