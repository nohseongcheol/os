#!/usr/bin/env python3
"""Apply this project's desktop files, retaining originals and user data."""
import hashlib
import json
from pathlib import Path
import shutil


def apply(payload, root=Path('/')):
    manifest = json.loads((payload / 'manifest.json').read_text())
    if (root / 'etc/jkoros-base-id').read_text().strip() != manifest['base_id']:
        raise RuntimeError('Desktop update does not match this system image')
    state = root / 'home/user/.jkoros/desktop-updates'
    marker = state / 'current.json'
    if marker.exists() and json.loads(marker.read_text()).get('version') == manifest['version']:
        return
    for entry in manifest['files']:
        relative = Path(entry['path'])
        if relative.is_absolute() or '..' in relative.parts:
            raise RuntimeError('Invalid desktop update path')
        data = (payload / 'files' / relative).read_bytes()
        if hashlib.sha256(data).hexdigest() != entry['sha256']:
            raise RuntimeError('Desktop update checksum mismatch: ' + str(relative))
    backup = state / manifest['version']
    for entry in manifest['files']:
        relative = Path(entry['path'])
        source, target = payload / 'files' / relative, root / relative
        if target.is_file() and not target.is_symlink() and source.read_bytes() == target.read_bytes():
            continue
        previous = backup / relative
        if (target.exists() or target.is_symlink()) and not (previous.exists() or previous.is_symlink()):
            previous.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(str(target), str(previous), follow_symlinks=False)
        target.parent.mkdir(parents=True, exist_ok=True)
        staged = target.with_name(target.name + '.jkoros-update')
        staged.write_bytes(source.read_bytes())
        staged.chmod(entry['mode'])
        staged.replace(target)
    state.mkdir(parents=True, exist_ok=True)
    staged = state / 'current.json.next'
    staged.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + '\n')
    staged.replace(marker)
    print('JKOROS_DESKTOP_UPDATED ' + manifest['version'], flush=True)


if __name__ == '__main__':
    apply(Path(__file__).resolve().parent)
