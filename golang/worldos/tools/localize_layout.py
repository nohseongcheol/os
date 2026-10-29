#!/usr/bin/env python3
"""Backed-up migration of edition-local management paths; default is dry-run.

Never regenerate kernels, replace user disks, or create compatibility symlinks.
Each edition is an independently verified/rollback-capable transaction.
"""
import argparse
import json
import os
from pathlib import Path
import shutil
import tempfile

from generate_script_variants import table
from install_shells import editions
from layout_terms import proposals
from management_layout import checksum, encoded, translate
from native_source import local_path, safe, verify as verify_variant
from posix_build import verify as verify_posix
from refine_country_names import verify as verify_country
from shell_build import verify as verify_shell
from worldos_vbox import validate as verify_vbox


def snapshot(tree):
    result = {}
    for current, directories, files in os.walk(str(tree)):
        directories[:] = [d for d in directories if d not in ('build', '__pycache__', '.git', '.vbox')]
        for name in directories:
            safe(tree, str((Path(current) / name).relative_to(tree)))
        for name in files:
            path = safe(tree, str((Path(current) / name).relative_to(tree)))
            result[str(path.relative_to(tree))] = (path.read_bytes(), path.stat().st_mode & 0o777)
    return result


def verified_components(parent):
    kernel = local_path(parent, '소스')
    variant = local_path(kernel, '문자대응.json')
    if variant.is_file():
        verify_variant(kernel, json.loads(variant.read_text(encoding='utf-8')))
    else:
        verify_country(kernel)
    posix = safe(parent, json.loads((parent / 'posix-entry.json').read_text(encoding='utf-8'))['directory'])
    shell = safe(parent, json.loads((parent / 'shell-entry.json').read_text(encoding='utf-8'))['directory'])
    verify_posix(posix, json.loads((posix / 'posix.json').read_text(encoding='utf-8')))
    verify_shell(shell, json.loads((shell / 'shell.json').read_text(encoding='utf-8')))
    verify_vbox(parent)  # Local entry checks only; never invokes VirtualBox.
    return kernel, posix, shell


def plan(root, record):
    edition, parent, language = record
    components = verified_components(parent)
    terms, status = proposals(language)
    kernel_name = terms['소스']
    old_kernel = components[0].name
    if kernel_name != old_kernel and ((parent / kernel_name).exists() or (parent / kernel_name).is_symlink()):
        raise RuntimeError('Refusing existing kernel destination: ' + str(parent / kernel_name))
    prepared = []
    renamed = []
    for index, directory in enumerate(components):
        before = snapshot(directory)
        inputs = dict(before)
        if index == 0 and local_path(directory, '문자대응.json').is_file():
            adapter = str(local_path(directory, '문자빌드.py').relative_to(directory))
            inputs[adapter] = ((root / 'tools/native_source.py').read_bytes(), before[adapter][1])
        elif index in (1, 2):
            for name in ('native_source.py', 'posix_build.py' if index == 1 else 'shell_build.py'):
                inputs[name] = ((root / 'tools' / name).read_bytes(), before[name][1])
        after, moves, _ = translate(inputs, language)
        if index == 0 and terms['문자대응.json'] in after:
            name = terms['문자대응.json']
            config = json.loads(after[name][0].decode('utf-8'))
            config['summary']['source'] = str((parent / kernel_name).relative_to(root))
            after[name] = (encoded(config), after[name][1])
        prepared.append((directory.name, before, after))
        renamed.extend([directory.name + '/' + old, (kernel_name if index == 0 else directory.name) + '/' + new]
                       for old, new in moves.items())
    before = {name: ((parent / name).read_bytes(), (parent / name).stat().st_mode & 0o777)
              for name in ('Makefile', 'vbox.py', 'vbox-entry.json')}
    if (parent / 'layout.json').exists():
        before['layout.json'] = ((parent / 'layout.json').read_bytes(), (parent / 'layout.json').stat().st_mode & 0o777)
    after = dict(before)
    make = before['Makefile'][0].decode('utf-8')
    for old in ('-C "' + old_kernel + '" ', '-C ' + old_kernel + ' '):
        make = make.replace(old, '-C "' + kernel_name + '" ')
    if '/'.join(edition.split('/')[1:]):
        # Script editions previously had no parent-level kernel entry.
        if '\nsource:' not in make and '\nkernel source:' not in make:
            make += '\n# WorldOS independent kernel entry\n.PHONY: source source-iso\nsource:\n\t$(MAKE) -C "' + kernel_name + '" kernel\nsource-iso:\n\t$(MAKE) -C "' + kernel_name + '" iso\n'
    after['Makefile'] = (make.encode('utf-8'), before['Makefile'][1])
    launcher = (root / 'tools/worldos_vbox.py').read_bytes()
    after['vbox.py'] = (launcher, before['vbox.py'][1])
    config = json.loads(before['vbox-entry.json'][0].decode('utf-8'))
    config['kernel_directory'] = kernel_name
    config['launcher_sha256'] = checksum(launcher)
    after['vbox-entry.json'] = (encoded(config), before['vbox-entry.json'][1])
    after['layout.json'] = (encoded({'version': 1, 'edition': edition, 'language': language,
        'status': status, 'paths': {'소스': kernel_name}}), 0o644)
    prepared.append(('', before, after))
    if old_kernel != kernel_name:
        renamed.insert(0, [old_kernel, kernel_name])
    return {'edition': edition, 'language': language, 'status': status, 'old_kernel': old_kernel,
            'kernel': kernel_name, 'components': prepared, 'renames': renamed,
            'changes': sum(sum(old.get(name) != value for name, value in new.items()) + len(set(old) - set(new))
                           for _, old, new in prepared)}


def publish(tree, before, after):
    for name, value in after.items():
        target = safe(tree, name)
        if name in before and before[name] == value:
            continue
        target.parent.mkdir(parents=True, exist_ok=True)
        data, mode = value
        with tempfile.NamedTemporaryFile(dir=str(target.parent), delete=False) as stream:
            temporary = Path(stream.name)
            stream.write(data)
        temporary.chmod(mode)
        os.replace(str(temporary), str(target))
    for old in sorted(set(before) - set(after)):
        safe(tree, old).unlink()  # Exact files copied to backup before publication.


def apply(root, record, migration, backup_root):
    edition, parent, _ = record
    backup = backup_root / edition
    backup.mkdir(parents=True, exist_ok=False)
    required = sum(len(data) for _, before, _ in migration['components'] for data, _ in before.values())
    if shutil.disk_usage(str(backup_root)).free < required * 2 + 256 * 1024 * 1024:
        raise RuntimeError('Insufficient free space for a recoverable migration: ' + edition)
    # Preflight every path before any write to the edition.
    for directory, before, after in migration['components']:
        tree = parent / directory
        for name, (data, _) in before.items():
            if safe(tree, name).read_bytes() != data:
                raise RuntimeError('Concurrent edit: ' + str(tree / name))
        for name in set(after) - set(before):
            if safe(tree, name).exists():
                raise RuntimeError('Refusing untracked destination: ' + str(tree / name))
    for directory, before, _ in migration['components']:
        for name, (data, mode) in before.items():
            destination = safe(backup, str(Path(directory) / name))
            destination.parent.mkdir(parents=True, exist_ok=True)
            destination.write_bytes(data)
            destination.chmod(mode)
    public = {key: value for key, value in migration.items() if key != 'components'}
    (backup / 'migration.json').write_bytes(encoded(public))
    written, moved = [], False
    try:
        for directory, before, after in migration['components']:
            written.append((directory, before, after))
            publish(parent / directory, before, after)
        if migration['old_kernel'] != migration['kernel']:
            safe(parent, migration['old_kernel']).rename(safe(parent, migration['kernel']))
            moved = True
        verified_components(parent)
    except Exception:
        if moved:
            safe(parent, migration['kernel']).rename(safe(parent, migration['old_kernel']))
        for directory, before, after in reversed(written):
            # Retain failure products in the recovery copy instead of discarding
            # potentially useful diagnostics from an interrupted publication.
            tree = parent / directory
            for name in set(after) - set(before):
                path = safe(tree, name)
                if path.is_file():
                    failed = safe(backup, str(Path('failed') / directory / name))
                    failed.parent.mkdir(parents=True, exist_ok=True)
                    shutil.move(str(path), str(failed))
            for name, (data, mode) in before.items():
                target = safe(tree, name)
                target.parent.mkdir(parents=True, exist_ok=True)
                target.write_bytes(data)
                target.chmod(mode)
        raise
    # Only obsolete empty metadata directories, never unknown contents/builds.
    for directory, before, after in migration['components']:
        directory = migration['kernel'] if directory == migration['old_kernel'] else directory
        obsolete_dirs = {p for name in set(before) - set(after) for p in Path(name).parents if str(p) != '.'}
        for name in sorted(obsolete_dirs, key=lambda p: len(p.parts), reverse=True):
            try:
                safe(parent / directory, name).rmdir()
            except OSError:
                pass
    print('APPLIED', edition, 'BACKUP', backup, flush=True)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root', type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument('--edition', action='append', default=[])
    parser.add_argument('--apply', action='store_true')
    parser.add_argument('--check', action='store_true')
    args = parser.parse_args()
    records = editions(args.root)
    if set(args.edition) - {r[0] for r in records}:
        parser.error('Unknown edition')
    selected = [r for r in records if not args.edition or r[0] in args.edition]
    backup_root = Path(tempfile.mkdtemp(prefix='worldos-layout-backup-')) if args.apply else None
    results = []
    for record in selected:
        migration = plan(args.root, record)
        if args.check and migration['changes']:
            raise RuntimeError('Outdated management layout: ' + record[0])
        if args.apply and migration['changes']:
            apply(args.root, record, migration, backup_root)
        results.append([record[0], record[2], migration['kernel'], migration['status'], len(migration['renames']), migration['changes']])
        print('CHECK' if args.check else 'PLAN', *results[-1], flush=True)
    if args.apply and not args.edition:
        (args.root / '관리경로-현지화.tsv').write_text(table(['edition', 'language', 'source_directory', 'review_status', 'renamed_paths', 'changed_files'], results), encoding='utf-8')
    print('TOTAL', len(results), 'editions', flush=True)


if __name__ == '__main__':
    main()
