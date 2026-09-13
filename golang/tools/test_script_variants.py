import json
from pathlib import Path
import tempfile
import unittest

from native_source import go_transform, asm_transform, inverse, safe, transform, stage
from generate_script_variants import profiles, label_name
from variant_terms import INDIA, terms, whole_names


class NativeScriptTests(unittest.TestCase):
    def test_india_22_unique(self):
        self.assertEqual(len(INDIA), 22)
        self.assertEqual(len({row[1] for row in INDIA}), 22)
        available = {p[1] for p in profiles() if p[0] == 'IND'}
        self.assertTrue(all(language + '_' + script in available for language, _, _, script in INDIA))

    def test_all_primary_profiles_have_terms(self):
        for language, _, _, script in INDIA:
            self.assertTrue(terms(language + '_' + script))

    def test_required_japanese_chinese(self):
        available = {(p[0], p[1]) for p in profiles()}
        for profile in ('ja_Jpan', 'ja_Hira', 'ja_Kana'):
            self.assertIn(('JPN', profile), available)
        for country in ('CHN', 'HKG', 'MAC', 'TWN'):
            for profile in ('zh_Hans', 'zh_Hant'):
                self.assertIn((country, profile), available)

    def test_combining_marks_roundtrip(self):
        for native in ('पढ़ना', 'স্মৃতি', 'முகவரிச்_சுட்டி', 'కేటాయించు', 'ലേഖനം', 'پَرُن', 'ꯄꯥꯕ', 'ᱚᱞ', 'ひらがな', 'カタカナ', 'क्षेत्र'):
            source = 'package main\nvar ' + native + ' = 1\n'
            compiled = go_transform(source, {native: 'identifier'}, {})
            self.assertIn('var identifier', compiled)
            self.assertEqual(go_transform(compiled, {'identifier': native}, {}), source)

    def test_literals_comments_numbers_untouched(self):
        source = 'var पढ़ना = 0xff + 1e-9 + .2i // पढ़ना\n/* पढ़ना */\nvar s = "पढ़ना"\nvar r = \'प\'\nvar raw = `पढ़ना`\n'
        result = go_transform(source, {'पढ़ना': 'Read', 'xff': 'BAD', 'e': 'BAD'}, {})
        self.assertEqual(result, source.replace('var पढ़ना', 'var Read'))

    def test_imports_only_not_runtime_strings(self):
        source = 'package main\nimport (\n. "स्मृति"\n)\nvar s = "स्मृति"\n'
        self.assertEqual(go_transform(source, {}, {'स्मृति': 'memory'}), source.replace('. "स्मृति"', '. "memory"'))

    def test_assembly_symbol_only(self):
        source = 'TEXT ·पढ़ना(SB),$0\n// ·पढ़ना\nMOVL $0xff, AX\n'
        self.assertEqual(asm_transform(source, {'पढ़ना': 'Read'}), source.replace('TEXT ·पढ़ना', 'TEXT ·Read'))

    def test_c_abi_bytes_preserved(self):
        data = b'int read(int fd); /* read */\n'
        self.assertEqual(transform(data, 'copy', {'read': 'different'}, {}, {}), data)

    def test_injective_maps(self):
        with self.assertRaises(ValueError):
            inverse({'Read': 'same', 'Write': 'same'})

    def test_unsafe_paths(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            for path in ('../outside', '/tmp/outside'):
                with self.assertRaises(ValueError):
                    safe(root, path)
            (root / 'link').symlink_to('/tmp', target_is_directory=True)
            with self.assertRaises(ValueError):
                safe(root, 'link/outside')

    def test_malformed_literals_rejected(self):
        for source in ('var x = "oops', '/* missing'):
            with self.assertRaises(ValueError):
                go_transform(source, {}, {})

    def test_native_vowel_signs_preserved(self):
        self.assertEqual(label_name('पढ़ना', 'Read'), 'Vपढ़ना')
        self.assertIn('கோப்பைப் படி', whole_names('ta_Taml').values())

    def test_edits_are_authoritative(self):
        with tempfile.TemporaryDirectory() as temporary:
            tree, destination = Path(temporary) / 'native', Path(temporary) / 'compiled'
            tree.mkdir()
            source = tree / 'मुख्य.go'
            source.write_text('package main\nvar Vपढ़ना = 7\n', encoding='utf-8')
            manifest = {'names': {'Read': 'Vपढ़ना'}, 'imports': {}, 'files': [
                {'native': 'मुख्य.go', 'compiler': 'main.go', 'kind': 'go', 'paths': {}, 'mode': 0o644}]}
            stage(tree, destination, manifest)
            self.assertIn('Read = 7', (destination / 'main.go').read_text())
            source.write_text('package main\nvar Vपढ़ना = 9\n', encoding='utf-8')
            stage(tree, destination, manifest)
            self.assertIn('Read = 9', (destination / 'main.go').read_text())

    def test_unregistered_sources_not_silently_ignored(self):
        with tempfile.TemporaryDirectory() as temporary:
            tree = Path(temporary)
            (tree / 'नई.go').write_text('package main', encoding='utf-8')
            with self.assertRaisesRegex(ValueError, 'Register new source'):
                stage(tree, tree / 'build', {'names': {}, 'imports': {}, 'files': []})

    def test_joiners_are_not_removed(self):
        name = 'क्ष\u200dेत्र'
        self.assertEqual(go_transform('var ' + name + ' = 1', {name: 'x'}, {}), 'var x = 1')

    def test_no_target_script_cross_contamination(self):
        # No Hindi proposal is used as a default for another language.
        self.assertEqual(terms('sat_Olck')['read'], 'ᱯᱟᱲᱦᱟᱣ')
        self.assertNotIn('memory', terms('sat_Olck'))


if __name__ == '__main__':
    unittest.main()
