#!/usr/bin/env python3
"""Prepare signed ARM64 packages locally, without changing the host OS."""
import hashlib
import argparse
import json
import shutil
import subprocess
import tarfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RELEASE = '3.24.2'
BRANCH = 'v3.24'
BASE = 'https://dl-cdn.alpinelinux.org/alpine/' + BRANCH
PACKAGES = '''alpine-baselayout alpine-keys apk-tools busybox busybox-static
ca-certificates linux-rpi linux-virt linux-firmware-brcm
openjdk25 python3 py3-pip py3-virtualenv gcc g++ musl-dev linux-headers
make binutils gdb git bash sudo coreutils tar gzip xz file curl nano
openssh-client e2fsprogs kmod util-linux wpa_supplicant wireless-tools
xorg-server xf86-video-fbdev xf86-input-libinput xinit xauth xterm openbox
xvfb xrandr eudev dbus font-noto font-noto-cjk font-noto-extra font-noto-all font-dejavu
fontconfig tzdata fcitx5 fcitx5-hangul fcitx5-m17n fcitx5-anthy
fcitx5-chinese-addons fcitx5-unikey m17n-db
mesa-dri-gallium mesa-gl mesa-egl adwaita-icon-theme gsettings-desktop-schemas
'''.split()


def digest(path):
    h = hashlib.sha256()
    with Path(path).open('rb') as f:
        for block in iter(lambda: f.read(1024 * 1024), b''):
            h.update(block)
    return h.hexdigest()


def download(url, target):
    target = Path(target)
    if not target.exists():
        part = target.with_name(target.name + '.download')
        subprocess.run(['curl', '-fL', '--retry', '3', '--max-time', '300',
                        '-o', str(part), url], check=True)
        part.replace(target)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--host-tools', action='store_true')
    parser.add_argument('--sdk-only', action='store_true', help='Only ARM64 headers/compiler libraries needed by the native kernel')
    args = parser.parse_args()
    vendor = ROOT / 'vendor'
    bootstrap = ROOT / 'build/bootstrap'
    rootfs = ROOT / 'build/rootfs'
    for p in (vendor, bootstrap / 'keys', rootfs):
        p.mkdir(parents=True, exist_ok=True)
    sources = []
    for kind in ('rpi', 'minirootfs'):
        name = 'alpine-{}-{}-aarch64.tar.gz'.format(kind, RELEASE)
        url = BASE + '/releases/aarch64/' + name
        download(url, vendor / name)
        download(url + '.sha256', vendor / (name + '.sha256'))
        expected = (vendor / (name + '.sha256')).read_text().split()[0]
        if digest(vendor / name) != expected:
            raise SystemExit('SHA256 mismatch: ' + name)
        sources.append({'file': name, 'url': url, 'sha256': expected})
    apk = vendor / 'apk-tools-static-3.0.8-r0.apk'
    download(BASE + '/main/x86_64/' + apk.name, apk)
    # This is a build-host executable. Target packages are verified by apk
    # against the release's trusted Alpine keys, with no --allow-untrusted.
    with tarfile.open(str(apk), 'r:gz', ignore_zeros=True) as archive:
        member = next(m for m in archive if m.isfile() and m.name.endswith('/apk.static'))
        (bootstrap / 'apk.static').write_bytes(archive.extractfile(member).read())
    (bootstrap / 'apk.static').chmod(0o755)
    mini = vendor / ('alpine-minirootfs-' + RELEASE + '-aarch64.tar.gz')
    with tarfile.open(str(mini), 'r:gz') as archive:
        for m in archive:
            if m.isfile() and '/etc/apk/keys/' in '/' + m.name.lstrip('./'):
                (bootstrap / 'keys' / Path(m.name).name).write_bytes(archive.extractfile(m).read())
    repos = bootstrap / 'repositories'
    repos.write_text(BASE + '/main\n' + BASE + '/community\n')
    if args.host_tools:
        hostmini = vendor / ('alpine-minirootfs-' + RELEASE + '-x86_64.tar.gz')
        hosturl = BASE + '/releases/x86_64/' + hostmini.name
        download(hosturl, hostmini)
        download(hosturl + '.sha256', hostmini.with_name(hostmini.name + '.sha256'))
        if digest(hostmini) != hostmini.with_name(hostmini.name + '.sha256').read_text().split()[0]:
            raise SystemExit('Host minirootfs SHA256 mismatch')
        with tarfile.open(str(hostmini), 'r:gz') as archive:
            for m in archive:
                if m.isfile() and '/etc/apk/keys/' in '/' + m.name.lstrip('./'):
                    (bootstrap / 'keys' / Path(m.name).name).write_bytes(archive.extractfile(m).read())
        host = ROOT / 'build/host'
        host.mkdir(exist_ok=True)
        subprocess.run([str(bootstrap / 'apk.static'), '--root', str(host),
                        '--arch', 'x86_64', '--usermode', '--no-chown', '--no-scripts',
                        '--keys-dir', str(bootstrap / 'keys'), '--repositories-file', str(repos),
                        '--initdb', '--update-cache', 'add', 'qemu-system-aarch64', 'qemu-aarch64', 'proot', 'openjdk25-jdk'], check=True)
        return
    cache = vendor / 'packages'
    cache.mkdir(exist_ok=True)
    subprocess.run([str(bootstrap / 'apk.static'), '--root', str(rootfs),
                    '--arch', 'aarch64', '--usermode', '--no-chown', '--no-scripts',
                    '--keys-dir', str(bootstrap / 'keys'), '--repositories-file', str(repos),
                    '--cache-dir', str(cache), '--cache-packages', '--initdb',
                    '--update-cache', 'add'] + (['gcc', 'musl-dev'] if args.sdk_only else PACKAGES), check=True)
    database = rootfs / 'lib/apk/db/installed'
    if not database.exists():
        database = rootfs / 'usr/lib/apk/db/installed'
    records = []
    for record in database.read_text().split('\n\n'):
        fields = dict(s.split(':', 1) for s in record.splitlines() if ':' in s)
        if 'P' in fields:
            records.append({k: fields.get(k, '') for k in ('P', 'V', 'A', 'C', 'L', 'U', 'o')})
    (ROOT / 'build/packages.lock.json').write_text(json.dumps(records, indent=2) + '\n')
    sources.append({'file': apk.name, 'url': BASE + '/main/x86_64/' + apk.name, 'sha256': digest(apk)})
    (ROOT / 'build/sources.lock.json').write_text(json.dumps(sources, indent=2) + '\n')
    (ROOT / ('build/sdk-prepared' if args.sdk_only else 'build/prepared')).write_text(digest(database) + '\n')
    test_packages = vendor / 'test-packages'
    test_packages.mkdir(exist_ok=True)
    subprocess.run([str(bootstrap / 'apk.static'), '--root', str(rootfs), '--arch', 'aarch64',
                    '--keys-dir', str(bootstrap / 'keys'), '--repositories-file', str(repos),
                    'fetch', '--output', str(test_packages), 'tree'], check=True)
    print('ARM64 packages installed:', len(records), flush=True)


if __name__ == '__main__':
    main()
