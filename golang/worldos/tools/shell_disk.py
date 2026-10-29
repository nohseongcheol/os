#!/usr/bin/env python3
"""Prepare a NEW shell test disk, never modifying the supplied original disk."""
import argparse
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import tempfile

from install_shells import editions
from native_source import safe, local_path


def run(command, **kwargs):
    return subprocess.check_output([str(item) for item in command], stderr=subprocess.STDOUT, **kwargs)


def find_shell(root, edition):
    record = next((row for row in editions(root) if row[0] == edition), None)
    if record is None:
        raise ValueError('Unknown edition: ' + edition)
    parent = record[1]
    entry = json.loads((parent / 'shell-entry.json').read_text(encoding='utf-8'))
    return parent, safe(parent, entry['directory'])


def install_programs(raw, package, files=()):
    layout = run(['sfdisk', '-d', raw]).decode()
    match = re.search(r'start=\s*(\d+)', layout)
    if not match or int(match.group(1)) <= 0:
        raise ValueError('No positive partition start in supplied disk')
    image = str(raw) + '@@' + str(int(match.group(1)) * 512)
    environment = dict(os.environ, MTOOLS_SKIP_CHECK='1')
    programs = [('worldos-shell', 'USER1'), ('worldos-idle', 'USER2'), ('worldos-idle', 'USER3'),
                ('worldos-shell-probe', 'SHEXEC')]
    for executable, name in programs:
        source = package / 'build' / executable
        if not source.is_file():
            raise ValueError('Build the shell before preparing a disk: ' + str(source))
        run(['mcopy', '-o', '-i', image, source, '::' + name], env=environment)
    for source, name in files:
        if not re.fullmatch(r'[A-Z0-9]{1,8}', name):
            raise ValueError('Test disk uses extensionless FAT short names')
        run(['mcopy', '-o', '-i', image, source, '::' + name], env=environment)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root', type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument('--edition', default='KOR')
    parser.add_argument('--source', required=True, type=Path)
    parser.add_argument('--output', required=True, type=Path)
    parser.add_argument('--command-file', type=Path, help='optional UTF-8 script installed as /COMMANDS in the new disk')
    args = parser.parse_args()
    if not args.source.is_file():
        parser.error('source disk must be an existing file')
    if args.output.exists() or args.output.is_symlink():
        parser.error('output must be a NEW file; existing disks are never overwritten')
    if args.command_file is not None and not args.command_file.is_file():
        parser.error('command file must be an existing file')
    parent, package = find_shell(args.root, args.edition)
    config = json.loads((package / 'shell.json').read_text(encoding='utf-8'))
    example = args.command_file or (safe(package, config['example_source']) if 'example_source' in config else None)
    if example is not None:
        example.read_text(encoding='utf-8')  # Reject malformed encoding before any build or disk operation.
    subprocess.check_call(['make', '-C', str(parent), 'shell'])
    subprocess.check_call(['make', '-B', '-C', str(local_path(parent, '소스')), 'iso'])
    args.output.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(prefix='shell-disk-', dir=str(args.output.parent)) as temporary:
        stage = Path(temporary)
        raw, disk = stage / 'disk.raw', stage / 'shell.vdi'
        run(['qemu-img', 'convert', '-O', 'raw', args.source, raw])
        install_programs(raw, package, [(example, 'COMMANDS')] if example else [])
        run(['qemu-img', 'convert', '-f', 'raw', '-O', 'vdi', raw, disk])
        # Atomic publication without overwriting a concurrent/new destination.
        os.link(str(disk), str(args.output))
    print('Created NEW shell disk:', args.output)
    print('Kernel ISO:', local_path(parent, '소스/build/kernel.iso'))
    print('Original disk was read only:', args.source)
    if example is not None:
        print('Guest command: source /commands')


if __name__ == '__main__':
    main()
