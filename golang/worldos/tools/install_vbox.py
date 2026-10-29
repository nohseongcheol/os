#!/usr/bin/env python3
"""Install independently runnable make vbox targets; preserve existing edits."""
import argparse
import hashlib
import json
from pathlib import Path
import re
import shutil
import tempfile

from install_shells import editions
from generate_script_variants import table
from worldos_vbox import validate, safe
from native_source import local_path

BEGIN = '# BEGIN WorldOS managed VirtualBox launcher'
END = '# END WorldOS managed VirtualBox launcher'
FRAGMENT = '''
# BEGIN WorldOS managed VirtualBox launcher
.PHONY: vbox vbox-prepare vbox-status vbox-check
export VBOX_BASE_DISK VBOX_VM_NAME VBOX_TYPE
vbox:
	python3 vbox.py run
vbox-prepare:
	python3 vbox.py prepare
vbox-status:
	python3 vbox.py status
vbox-check:
	python3 vbox.py check
# END WorldOS managed VirtualBox launcher
'''


def install(root, record, base_disk, refresh=False, check=False):
    edition, parent, _ = record
    makefile = safe(parent, 'Makefile')
    original_make = makefile.read_text(encoding='utf-8')
    entry_file = safe(parent, 'vbox-entry.json')
    script = safe(parent, 'vbox.py')
    previous = None
    if entry_file.exists():
        previous = json.loads(entry_file.read_text(encoding='utf-8'))
        validate(parent)
        if original_make.count(FRAGMENT) != 1:
            raise RuntimeError('Managed Makefile block changed: ' + str(makefile))
        if check:
            if script.read_bytes() != (root / 'tools/worldos_vbox.py').read_bytes():
                raise RuntimeError('Outdated VirtualBox helper: ' + edition)
            return previous
        if not refresh:
            return previous
    elif check:
        raise RuntimeError('Missing VirtualBox launcher: ' + edition)
    elif script.exists() or BEGIN in original_make or re.search(r'(?m)^vbox(?:-prepare|-status|-check)?\s*:', original_make):
        raise RuntimeError('Existing launcher/target needs manual review: ' + edition)
    source = (root / 'tools/worldos_vbox.py').read_bytes()
    config = {'version': 1, 'edition': edition, 'vm_name': 'worldos ' + edition.replace('/', ' '),
              'base_disk': str(base_disk), 'launcher_sha256': hashlib.sha256(source).hexdigest(),
              'kernel_directory': str(local_path(parent, '소스').relative_to(parent))}
    if previous:
        config['base_disk'] = previous['base_disk']
        config['vm_name'] = previous['vm_name']
    backup = Path(tempfile.mkdtemp(prefix='worldos-vbox-install-backup-'))
    for path in (makefile, script, entry_file):
        if path.exists():
            shutil.copy2(str(path), str(backup / path.name))
    if makefile.read_text(encoding='utf-8') != original_make:
        raise RuntimeError('Makefile changed during installation')
    script.write_bytes(source)
    entry_file.write_text(json.dumps(config, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    if not previous:
        makefile.write_text(original_make + FRAGMENT, encoding='utf-8')
    validate(parent)
    print('INSTALLED', edition, 'BACKUP', backup, flush=True)
    return config


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root', type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument('--base-disk', type=Path, default=Path('/home/user/VirtualBox VMs/eng operating system/NewVirtualDisk1-fixed-20260908.vdi'))
    parser.add_argument('--edition', action='append', default=[])
    parser.add_argument('--refresh', action='store_true')
    parser.add_argument('--check', action='store_true')
    args = parser.parse_args()
    records = editions(args.root)
    if set(args.edition) - {row[0] for row in records}:
        parser.error('Unknown edition')
    results = []
    for record in records:
        if not args.edition or record[0] in args.edition:
            config = install(args.root, record, args.base_disk.resolve(), args.refresh, args.check)
            results.append([record[0], str(record[1].relative_to(args.root)), config['vm_name'], 'PASS'])
    if args.check:
        print('PASS', len(results), 'independent VirtualBox launchers')
    elif not args.edition:
        (args.root / 'VirtualBox-목록.tsv').write_text(table(['edition', 'directory', 'vm_name', 'entry_check'], results), encoding='utf-8')


if __name__ == '__main__':
    main()
