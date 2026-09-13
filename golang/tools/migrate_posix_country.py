#!/usr/bin/env python3
"""Move audited POSIX packages to country-code paths without dropping user files."""
import argparse
import json
from pathlib import Path
import shutil
import tempfile

from install_shells import editions
from install_posix import addition, package_directory
from native_source import safe
from posix_build import verify


def directory(edition):
    return package_directory(edition)


def migrate(root, record):
    edition, parent, language = record
    entry_file = parent / 'posix-entry.json'
    entry_data = entry_file.read_bytes()
    entry = json.loads(entry_data.decode('utf-8'))
    source = safe(parent, entry['directory'])
    target = safe(parent, directory(edition))
    config = json.loads((source / 'posix.json').read_text(encoding='utf-8'))
    verify(source, config)
    if source == target:
        return None
    if target.exists() or target.is_symlink():
        raise RuntimeError('Refusing occupied country-code destination: ' + str(target))
    makefile = parent / 'Makefile'
    make_data = makefile.read_bytes()
    old = addition(entry['directory']).encode('utf-8')
    if make_data.count(old) != 1:
        raise RuntimeError('POSIX parent targets were edited: ' + str(makefile))
    # Full package backup includes build outputs and untracked user files.
    backup = Path(tempfile.mkdtemp(prefix='worldos-posix-country-backup-'))
    shutil.copytree(str(source), str(backup / source.name), symlinks=True)
    (backup / 'posix-entry.json').write_bytes(entry_data)
    (backup / 'Makefile').write_bytes(make_data)
    verify(source, config)
    if entry_file.read_bytes() != entry_data or makefile.read_bytes() != make_data:
        raise RuntimeError('Parent changed while backing up')
    source.rename(target)
    try:
        config['summary']['directory'] = str(target.relative_to(root))
        (target / 'posix.json').write_text(json.dumps(config, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
        entry['directory'] = target.name
        entry_file.write_text(json.dumps(entry, ensure_ascii=False) + '\n', encoding='utf-8')
        makefile.write_bytes(make_data.replace(old, addition(target.name).encode('utf-8')))
        verify(target, config)
    except Exception:
        shutil.copy2(str(backup / source.name / 'posix.json'), str(target / 'posix.json'))
        target.rename(source)
        entry_file.write_bytes(entry_data)
        makefile.write_bytes(make_data)
        raise
    print('MOVED', edition, source.name, '->', target.name, 'BACKUP', backup, flush=True)
    return str(backup)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root', type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument('--edition', action='append', default=[])
    args = parser.parse_args()
    records = editions(args.root)
    if set(args.edition) - {r[0] for r in records}:
        parser.error('Unknown edition')
    for record in records:
        if not args.edition or record[0] in args.edition:
            migrate(args.root, record)


if __name__ == '__main__':
    main()
