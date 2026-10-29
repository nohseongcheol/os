"""Check update integrity and preservation without touching real user homes."""
import configparser
import hashlib
import importlib.util
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch


RUNTIME = Path(__file__).resolve().parents[1] / 'runtime'


def module(name):
    spec = importlib.util.spec_from_file_location(name, RUNTIME / (name + '.py'))
    loaded = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(loaded)
    return loaded


class DesktopUpdateTest(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name) / 'root'
        self.payload = Path(self.temporary.name) / 'payload'
        (self.root / 'etc').mkdir(parents=True)
        (self.root / 'etc/jkoros-base-id').write_text('test-base\n')
        (self.root / 'etc/desktop').write_text('original\n')
        (self.payload / 'files/etc').mkdir(parents=True)
        (self.payload / 'files/etc/desktop').write_text('updated\n')
        self.manifest = {'base_id': 'test-base', 'version': 'test-update', 'files': [
            {'path': 'etc/desktop', 'mode': 0o644,
             'sha256': hashlib.sha256(b'updated\n').hexdigest()}]}
        self.save_manifest()

    def save_manifest(self):
        (self.payload / 'manifest.json').write_text(json.dumps(self.manifest))

    def apply(self):
        module('apply-desktop-update').apply(self.payload, self.root)

    def test_backup_and_idempotence_preserve_later_user_edits(self):
        self.apply()
        backup = self.root / 'home/user/.jkoros/desktop-updates/test-update/etc/desktop'
        self.assertEqual(backup.read_text(), 'original\n')
        self.assertEqual((self.root / 'etc/desktop').read_text(), 'updated\n')
        (self.root / 'etc/desktop').write_text('user customization\n')
        self.apply()
        self.assertEqual((self.root / 'etc/desktop').read_text(), 'user customization\n')
        self.assertEqual(backup.read_text(), 'original\n')

    def test_corrupt_payload_leaves_original_untouched(self):
        (self.payload / 'files/etc/desktop').write_text('corrupt')
        with self.assertRaisesRegex(RuntimeError, 'checksum'):
            self.apply()
        self.assertEqual((self.root / 'etc/desktop').read_text(), 'original\n')

    def test_wrong_base_leaves_original_untouched(self):
        self.manifest['base_id'] = 'different-base'
        self.save_manifest()
        with self.assertRaisesRegex(RuntimeError, 'does not match'):
            self.apply()
        self.assertEqual((self.root / 'etc/desktop').read_text(), 'original\n')

    def test_settings_merge_preserves_custom_hotkeys_and_backups(self):
        home = self.root / 'home/user'
        config_dir = home / '.config/fcitx5'
        config_dir.mkdir(parents=True)
        original = '[Hotkey/TriggerKeys]\n0=Super+space\n[Behavior]\nCustom=True\n'
        (config_dir / 'config').write_text(original)
        (config_dir / 'profile').write_text(
            '[Groups/0]\nName=Personal\n[Groups/0/Items/0]\nName=keyboard-us\n')
        settings = module('desktop-settings')
        with patch.object(settings.Path, 'home', return_value=home):
            settings.main()
        result = configparser.ConfigParser()
        result.read(str(config_dir / 'config'))
        self.assertEqual(set(result['Hotkey/TriggerKeys'].values()),
                         {'Super+space', 'Control+space', 'Hangul'})
        self.assertEqual(result['Behavior']['Custom'], 'True')
        state = home / '.local/state/jkoros/desktop-settings'
        backup = state / (state / 'version').read_text().strip()
        self.assertEqual((backup / 'config').read_text(), original)
        (config_dir / 'config').write_text('customized after update\n')
        with patch.object(settings.Path, 'home', return_value=home):
            settings.main()
        self.assertEqual((config_dir / 'config').read_text(), 'customized after update\n')


if __name__ == '__main__':
    unittest.main()
