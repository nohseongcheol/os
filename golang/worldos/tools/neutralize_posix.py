#!/usr/bin/env python3
"""Migrate only audited POSIX implementation names; keep historical evidence."""
import argparse
import hashlib
import json
from pathlib import Path
import shutil
import tempfile

from install_shells import editions
from generate_script_variants import rows, table
from native_source import safe, transform, inverse, local_path, verify as verify_variant
from refine_country_names import verify as verify_country


def sha(data):
    return hashlib.sha256(data).hexdigest()


def neutral(text):
    return (text.replace('__engos_syscall6', '__syscall6')
            .replace('__engos_syscall_result', '__syscall_result')
            .replace('libengos_posix.a', 'libposix.a')
            .replace('engos/syscall.h', 'sys/syscall.h')
            .replace('_ENGOS_', '_LIBC_').replace('ENGOS=1', 'POSIX_TEST=1')
            .replace('text_equal(name.sysname, "EngOS")', 'name.sysname[0] != 0')
            .replace('text_equal(name.nodename, "engos")', 'name.nodename[0] != 0'))


def migrate(record, backup):
    edition, parent, _ = record
    tree = local_path(parent, '소스')
    variant = local_path(tree, '문자대응.json').is_file()
    audit_file = local_path(tree, '문자대응.json' if variant else '명명검증.json')
    audit = json.loads(audit_file.read_text(encoding='utf-8'))
    if variant:
        verify_variant(tree, audit)
    else:
        verify_country(tree)
    path_file = local_path(tree, '파일대응표.tsv')
    mapping = rows(path_file)
    changes = []
    for row in mapping[1:]:
        original, relative = row
        if not original.startswith('userland/posix/') or original.endswith('.md'):
            continue
        before = safe(tree, relative).read_bytes()
        after = neutral(before.decode('utf-8')).encode('utf-8')
        renamed = relative.replace('/engos/syscall.h', '/sys/syscall.h')
        if before != after or relative != renamed:
            if renamed != relative and safe(tree, renamed).exists():
                raise RuntimeError('Destination already exists: ' + renamed)
            changes.append((relative, renamed, before, after))
            row[1] = renamed
    # The obsolete namespace directory may remain after an earlier migration.
    # rmdir is deliberately non-recursive: user-added contents are preserved.
    for original, relative in mapping[1:]:
        if original == 'userland/posix/include/engos/syscall.h' and '/sys/syscall.h' in relative:
            old_directory = safe(tree, str(Path(relative).parent.parent / 'engos'))
            if old_directory.is_dir() and not any(old_directory.iterdir()):
                old_directory.rmdir()
    if not changes:
        return False
    destination = backup / edition
    destination.mkdir(parents=True)
    shutil.copy2(str(audit_file), str(destination / audit_file.name))
    shutil.copy2(str(path_file), str(destination / path_file.name))
    for old, new, before, after in changes:
        target = safe(destination, old)
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(before)
        if safe(tree, old).read_bytes() != before:
            raise RuntimeError('Source changed during migration: ' + old)
    for old, new, before, after in changes:
        if old != new:
            safe(tree, new).parent.mkdir(parents=True, exist_ok=True)
            safe(tree, old).rename(safe(tree, new))
        safe(tree, new).write_bytes(after)
        if variant:
            entry = next(entry for entry in audit['files'] if entry['native'] == old)
            entry['native'] = new
            entry['compiler'] = neutral(entry['compiler'])
            entry['sha256'] = sha(after)
        else:
            audit['hashes'].pop(old)
            audit['hashes'][new] = sha(after)
    if variant:
        for entry in audit['files']:
            entry['paths'] = {neutral(k): neutral(v) for k, v in entry['paths'].items()}
            data = safe(tree, entry['native']).read_bytes()
            entry['compiler_sha256'] = sha(transform(data, entry['kind'], inverse(audit['names']), inverse(audit['imports']), inverse(entry['paths'])))
    path_file.write_text(table(mapping[0], mapping[1:]), encoding='utf-8')
    if not variant and path_file.name in audit['hashes']:
        audit['hashes'][path_file.name] = sha(path_file.read_bytes())
    audit.setdefault('functional_fixes', {})['neutral-posix-v1'] = {
        'backup': str(destination), 'files': [new for _, new, _, _ in changes],
        'note': 'Implementation namespace only; uname validates identity without hardcoding donor OS.'}
    audit_file.write_text(json.dumps(audit, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    return True


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root', type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument('--edition', action='append', default=[])
    args = parser.parse_args()
    records = editions(args.root)
    if set(args.edition) - {row[0] for row in records}:
        parser.error('Unknown edition')
    backup = Path(tempfile.mkdtemp(prefix='worldos-posix-neutral-backup-'))
    print('Backup:', backup, flush=True)
    for record in records:
        if not args.edition or record[0] in args.edition:
            print('MIGRATED' if migrate(record, backup) else 'UNCHANGED', record[0], flush=True)


if __name__ == '__main__':
    main()
