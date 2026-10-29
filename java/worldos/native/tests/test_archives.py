import json
import os
from pathlib import Path
import shutil
import sys
import tempfile
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from archives import ARCHIVES, archive_writer, copy_archive, materialize, publish_archive, sha256
from export import export_country


class ArchiveTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory(prefix='worldos archive test ')
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name) / 'worldos'
        self.common = self.root / 'native/resources'
        self.common.mkdir(parents=True)
        for name in ARCHIVES:
            (self.common / name).write_bytes(('archive ' + name).encode())
        self.country('KOR')
        self.country('JPN')

    def country(self, code):
        folder = self.root / 'country' / code
        folder.mkdir(parents=True)
        config = {'country': code, 'source': 'source'}
        for name, key in ARCHIVES.items():
            (folder / name).symlink_to(os.path.relpath(str(self.common / name), str(folder)))
            config[key] = sha256(folder / name)
        (folder / 'native.json').write_text(json.dumps(config))
        example = folder / 'source/example/test.java'
        example.parent.mkdir(parents=True)
        example.write_text('source')
        manifest = {name: sha256(folder / name) for name in ['native.json', 'source/example/test.java']}
        (folder / 'native-generated.json').write_text(json.dumps(manifest))
        return folder

    def test_materialized_countries_are_independent_after_move(self):
        report = materialize(self.root)
        self.assertGreaterEqual(report['copies_created'], 4)
        self.assertEqual(materialize(self.root)['copies_created'], 0)
        moved = self.root.parent / 'moved tree'
        self.root.rename(moved)
        first = moved / 'country/KOR/native-vendor.tar.gz'
        second = moved / 'country/JPN/native-vendor.tar.gz'
        self.assertFalse(first.is_symlink())
        self.assertNotEqual(first.stat().st_ino, second.stat().st_ino)
        self.assertEqual(first.stat().st_mode & 0o777, 0o644)
        first.write_bytes(b'local change')
        self.assertEqual(second.read_bytes(), b'archive native-vendor.tar.gz')

    def test_bad_country_checksum_changes_no_other_country(self):
        path = self.root / 'country/KOR/native-vendor.tar.gz'
        path.unlink(); path.write_bytes(b'changed user archive')
        with self.assertRaisesRegex(ValueError, 'checksum mismatch'):
            materialize(self.root)
        self.assertTrue((self.root / 'country/JPN/native-vendor.tar.gz').is_symlink())
        self.assertEqual(path.read_bytes(), b'changed user archive')

    def test_distinct_country_versions_are_preserved(self):
        folder = self.root / 'country/KOR'
        path = folder / 'native-vendor.tar.gz'
        path.unlink(); path.write_bytes(b'country-specific release')
        config = json.loads((folder / 'native.json').read_text())
        config['vendor_sha256'] = sha256(path)
        (folder / 'native.json').write_text(json.dumps(config))
        materialize(self.root)
        self.assertEqual(path.read_bytes(), b'country-specific release')
        self.assertNotEqual(path.stat().st_ino, (self.root / 'country/JPN/native-vendor.tar.gz').stat().st_ino)

    def test_new_release_does_not_change_other_countries(self):
        materialize(self.root)
        alias = self.common / 'native-vendor.tar.gz'
        with archive_writer(alias) as staged:
            staged.write_bytes(b'new vendor release')
        published = publish_archive(alias)
        self.assertFalse(published.is_symlink())
        copy_archive(self.root / 'country/KOR/native-vendor.tar.gz', published, sha256(published))
        self.assertEqual((self.root / 'country/JPN/native-vendor.tar.gz').read_bytes(), b'archive native-vendor.tar.gz')

    def test_failed_rebuild_keeps_previous_release(self):
        alias = self.common / 'native-vendor.tar.gz'
        original = alias.read_bytes()
        with self.assertRaisesRegex(RuntimeError, 'failed build'):
            with archive_writer(alias) as staged:
                staged.write_bytes(b'incomplete')
                raise RuntimeError('failed build')
        self.assertEqual(alias.read_bytes(), original)

    def test_export_remains_independent(self):
        materialize(self.root)
        original = self.root / 'country/KOR'
        destination = self.root.parent / 'exported country'
        export_country(original, destination)
        shutil.rmtree(str(self.root))
        config = json.loads((destination / 'native.json').read_text())
        for name, key in ARCHIVES.items():
            self.assertFalse((destination / name).is_symlink())
            self.assertEqual(sha256(destination / name), config[key])
        self.assertTrue((destination / 'example/test.java').is_file())

    def test_export_refuses_existing_destination(self):
        destination = self.root.parent / 'existing'
        destination.mkdir()
        (destination / 'keep').write_text('user file')
        with self.assertRaises(FileExistsError):
            export_country(self.root / 'country/KOR', destination)
        self.assertEqual((destination / 'keep').read_text(), 'user file')

    def test_export_freezes_effective_ip_override(self):
        materialize(self.root)
        original=self.root/'country/KOR'
        defaults=original/'source/ip.conf';defaults.write_text('IP=192.168.0.100\n')
        manifest=json.loads((original/'native-generated.json').read_text())
        manifest['source/ip.conf']=sha256(defaults)
        (original/'native-generated.json').write_text(json.dumps(manifest))
        (original/'ip.conf').write_text('IP=192.168.0.123\n')
        destination=self.root.parent/'exported configuration'
        export_country(original,destination)
        self.assertIn('IP=192.168.0.123\n',(destination/'ip.conf').read_text())
        exported=json.loads((destination/'native-generated.json').read_text())
        self.assertEqual(exported['ip.conf'],sha256(destination/'ip.conf'))


if __name__ == '__main__':
    unittest.main()
