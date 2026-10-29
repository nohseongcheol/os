import json
from pathlib import Path
import shutil
import tempfile
import unittest
from unittest.mock import patch

from layout_terms import ROWS, KEYS, proposals
from management_layout import translate
from native_source import local_path
from localize_layout import snapshot, plan, apply, verified_components, publish


class LayoutTests(unittest.TestCase):
    def test_language_rows_and_script_forms(self):
        for language in list(ROWS) + ['ja_Jpan', 'ja_Kana', 'hi_Deva', 'ta_Taml', 'und']:
            names, status = proposals(language)
            self.assertEqual(set(names), set(KEYS))
            self.assertEqual(len(names), len(set(names.values())))
            self.assertTrue(all(len(name.encode('utf-8')) <= 250 for name in names.values()))
            self.assertEqual(status, 'pending-language-review' if language == 'und' else 'project-proposal')
        self.assertEqual(proposals('zh_Hans')[0]['소스'], '源代码')
        self.assertEqual(proposals('zh_Hant')[0]['소스'], '原始碼')
        for language, low, high in [('ja_Hira', 0x3041, 0x3096), ('ja_Kana', 0x30a1, 0x30f6)]:
            for value in proposals(language)[0].values():
                self.assertTrue(all(low <= ord(c) <= high for c in Path(value).stem))

    def test_legacy_fallback_and_nested_resolution(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            self.assertEqual(local_path(root, '소스/build/kernel.iso'), root / '소스/build/kernel.iso')
            (root / 'layout.json').write_text(json.dumps({'version': 1, 'paths': {'소스': '源代码'}}))
            self.assertEqual(local_path(root, '소스/build/kernel.iso'), root / '源代码/build/kernel.iso')
            with self.assertRaises(ValueError):
                local_path(root, '../outside')
            (root / 'layout.json').write_text(json.dumps({'version': 1, 'paths': {'소스': '../outside'}}))
            with self.assertRaises(ValueError):
                local_path(root, '소스')

    def test_local_registry_refuses_symlinks(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            (root / 'target').write_text('{}')
            (root / 'layout.json').symlink_to(root / 'target')
            with self.assertRaises(ValueError):
                local_path(root, '소스')

    def test_path_collision_is_not_overwritten(self):
        with self.assertRaisesRegex(ValueError, 'collides'):
            translate({'이름대응표.tsv': (b'a', 0o644), '名称对应表.tsv': (b'user', 0o644)}, 'zh_Hans')

    def test_inherited_metadata_and_idempotence(self):
        initial = {'원본자료/용어사전.tsv': (b'original\n', 0o644), '원본자료/note.txt': (b'keep', 0o644)}
        updated, moves, _ = translate(initial, 'zh_Hans')
        self.assertEqual(updated['继承资料/术语词表.tsv'][0], b'original\n')
        self.assertEqual(updated['继承资料/note.txt'][0], b'keep')
        again, moves, _ = translate(updated, 'zh_Hans')
        self.assertEqual(updated, again)
        self.assertEqual(moves, {})

    def fixture(self, root, variant=False):
        repository = Path(__file__).resolve().parents[1]
        source_parent = repository / ('문자판/CHN/zh_Hans' if variant else '나라/CHN')
        parent = root / ('문자판/CHN/zh_Hans' if variant else '나라/CHN')
        shutil.copytree(str(source_parent), str(parent), ignore=shutil.ignore_patterns('build', '.vbox', '__pycache__'))
        (root / 'tools').mkdir()
        for name in ('native_source.py', 'posix_build.py', 'shell_build.py', 'worldos_vbox.py'):
            shutil.copy2(str(repository / 'tools' / name), str(root / 'tools' / name))
        return ('CHN/zh_Hans' if variant else 'CHN', parent, 'zh_Hans')

    def test_whole_edition_migration_keeps_user_file_and_rolls_back(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            record = self.fixture(root)
            parent = record[1]
            (local_path(parent, '소스') / 'user-note.txt').write_text('keep this')
            original = snapshot(parent)
            migration = plan(root, record)
            real_publish = publish
            def interrupted(tree, before, after):
                real_publish(tree, before, after)
                if tree.name == 'posix-CHN':
                    raise OSError('simulated publication interruption')
            with patch('localize_layout.publish', side_effect=interrupted):
                with self.assertRaisesRegex(OSError, 'simulated'):
                    apply(root, record, migration, root / 'failed-backup')
            self.assertEqual(snapshot(parent), original)
            verified_components(parent)
            apply(root, record, migration, root / 'backup')
            verified_components(parent)
            self.assertEqual((parent / '源代码/user-note.txt').read_text(), 'keep this')
            self.assertTrue((parent / '源代码/名称对应表.tsv').is_file())
            self.assertFalse((parent / '소스').exists())
            self.assertEqual(plan(root, record)['changes'], 0)

    def test_script_edition_keeps_compiler_input_and_build_entry(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            record = self.fixture(root, variant=True)
            migration = plan(root, record)
            apply(root, record, migration, root / 'backup')
            verified_components(record[1])
            kernel = local_path(record[1], '소스')
            self.assertTrue((kernel / '文字构建.py').is_file())
            self.assertIn('python3 文字构建.py', (kernel / 'Makefile').read_text())
            self.assertIn('-C "源代码" kernel', (record[1] / 'Makefile').read_text())
            self.assertEqual(plan(root, record)['changes'], 0)


if __name__ == '__main__':
    unittest.main()
