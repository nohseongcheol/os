#!/usr/bin/env python3
"""Install signed Alpine packages into an unprivileged project root directory."""
import hashlib
import json
from pathlib import Path
import subprocess
import tarfile

ROOT = Path(__file__).resolve().parents[1]
PACKAGES = [
    'alpine-baselayout', 'alpine-keys', 'apk-tools', 'busybox', 'busybox-extras',
    'ca-certificates', 'linux-virt', 'openjdk25',
    'xorg-server', 'xf86-video-fbdev', 'xf86-input-libinput', 'xvfb',
    'xinit', 'xterm', 'openbox', 'eudev', 'dbus', 'font-noto', 'font-noto-cjk',
    'font-noto-extra', 'font-noto-all', 'font-dejavu', 'fontconfig', 'tzdata', 'e2fsprogs',
    'gcc', 'musl-dev', 'linux-headers', 'make', 'binutils', 'kmod',
    'ibus', 'ibus-hangul', 'm17n-db', 'adwaita-icon-theme', 'gsettings-desktop-schemas',
    'fcitx5', 'fcitx5-m17n', 'fcitx5-hangul', 'fcitx5-anthy',
    'fcitx5-chinese-addons', 'fcitx5-unikey', 'fcitx5-rime',
    'mesa-dri-gallium', 'mesa-gl',
]

def main():
    target = ROOT / 'build/rootfs'
    keys = ROOT / 'build/bootstrap/keys'
    keys.mkdir(parents=True, exist_ok=True)
    # apk-tools uses concatenated signed tar streams; ignore_zeros reads them all.
    bootstrap = ROOT / 'build/bootstrap/apk.static'
    with tarfile.open(str(ROOT / 'vendor/apk-tools-static-3.0.8-r0.apk'), 'r:gz', ignore_zeros=True) as archive:
        member = next(item for item in archive if item.isfile() and item.name.endswith('/apk.static'))
        bootstrap.write_bytes(archive.extractfile(member).read())
        bootstrap.chmod(0o755)
    with tarfile.open(str(ROOT / 'vendor/alpine-minirootfs-3.24.1-x86_64.tar.gz'), 'r:gz') as archive:
        for member in archive:
            if member.isfile() and '/etc/apk/keys/' in '/' + member.name.lstrip('./'):
                (keys / Path(member.name).name).write_bytes(archive.extractfile(member).read())
    target.mkdir(parents=True, exist_ok=True)
    repositories = ROOT / 'build/bootstrap/repositories'
    repositories.write_text('https://dl-cdn.alpinelinux.org/alpine/v3.24/main\nhttps://dl-cdn.alpinelinux.org/alpine/v3.24/community\n')
    command = [str(ROOT / 'build/bootstrap/apk.static'), '--root', str(target),
               '--arch', 'x86_64', '--usermode', '--no-chown', '--no-scripts',
               '--keys-dir', str(keys), '--repositories-file', str(repositories),
               '--initdb', '--update-cache', 'add'] + PACKAGES
    subprocess.run(command, check=True)
    installed = target / 'lib/apk/db/installed'
    if not installed.exists():
        installed = target / 'usr/lib/apk/db/installed'
    records = []
    for entry in installed.read_text().split('\n\n'):
        fields = dict(line.split(':', 1) for line in entry.splitlines() if ':' in line)
        if 'P' in fields:
            records.append({key: fields.get(key, '') for key in ('P', 'V', 'C', 'L', 'U', 'o')})
    (ROOT / 'vendor/packages.lock.json').write_text(json.dumps(records, indent=2) + '\n')
    (ROOT / 'runtime/packages.lock.json').write_text(json.dumps(records, indent=2) + '\n')
    (ROOT / 'runtime/sources.lock.json').write_bytes((ROOT / 'vendor/sources.json').read_bytes())
    (ROOT / 'build/runtime-installed').write_text(hashlib.sha256(installed.read_bytes()).hexdigest() + '\n')
    print('Installed signed runtime packages:', len(records), flush=True)

if __name__ == '__main__':
    main()
