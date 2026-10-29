#!/usr/bin/env python3
"""Keep each country's pinned native archives as independent regular files."""
import argparse
from contextlib import contextmanager
import hashlib
import json
from pathlib import Path
import shutil
import tempfile

ROOT = Path(__file__).resolve().parents[1]
ARCHIVES = {'native-vendor.tar.gz': 'vendor_sha256',
            'qemu-host.tar.gz': 'qemu_sha256'}


def sha256(path):
    digest = hashlib.sha256()
    with Path(path).open('rb') as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b''):
            digest.update(chunk)
    return digest.hexdigest()


def copy_archive(destination, source, expected):
    """Install a verified, separately writable copy without exposing partial data."""
    destination, source = Path(destination), Path(source)
    if sha256(source) != expected:
        raise ValueError('Archive checksum mismatch: ' + str(source))
    if destination.is_file() and not destination.is_symlink():
        if destination.stat().st_nlink == 1 and sha256(destination) == expected:
            if destination.stat().st_mode & 0o777 != 0o644:
                destination.chmod(0o644)
                return True
            return False
    destination.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(prefix='.archive-copy-', dir=str(destination.parent)) as temporary:
        staged = Path(temporary) / destination.name
        shutil.copy2(str(source), str(staged))
        if sha256(staged) != expected:
            raise ValueError('Archive changed while copying: ' + str(source))
        staged.chmod(0o644)
        staged.replace(destination)
    return True


def publish_archive(alias, expected=None):
    """Turn an old shared alias into a regular file, preserving its bytes."""
    alias = Path(alias)
    digest = sha256(alias)
    if expected is not None and digest != expected:
        raise ValueError('Archive checksum mismatch: ' + str(alias))
    copy_archive(alias, alias, digest)
    return alias


@contextmanager
def archive_writer(alias):
    """Build a regular archive beside the old one and replace it atomically."""
    alias = Path(alias)
    alias.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(prefix='.archive-build-', dir=str(alias.parent)) as temporary:
        staged = Path(temporary) / alias.name
        yield staged
        if not staged.is_file():
            raise ValueError('Archive build produced no file: ' + str(alias))
        staged.replace(alias)


def materialize(root=ROOT):
    """Check every version before replacing shared links with independent copies."""
    root = Path(root)
    entries = []
    for config_path in sorted((root / 'country').glob('*/native.json')):
        config = json.loads(config_path.read_text(encoding='utf-8'))
        for name, key in ARCHIVES.items():
            path = config_path.parent / name
            if sha256(path) != config[key]:
                raise ValueError('Archive checksum mismatch: ' + str(path))
            entries.append((path, config[key]))
    for name in ARCHIVES:
        path = root / 'native/resources' / name
        entries.append((path, sha256(path)))
    changed = sum(copy_archive(path, path, digest) for path, digest in entries)
    return {'countries': (len(entries) - len(ARCHIVES)) // len(ARCHIVES),
            'archives_checked': len(entries), 'copies_created': changed}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('action', choices=['materialize'])
    args = parser.parse_args()
    if args.action == 'materialize':
        print(json.dumps(materialize(), indent=2))


if __name__ == '__main__':
    main()
