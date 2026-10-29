#!/usr/bin/env python3
import gzip
import hashlib
import json
import os
from pathlib import Path
import shutil
import stat
import subprocess
import sys
from archive import cpio, directory_entries

ROOT = Path(__file__).resolve().parents[1]

def main():
    filesystem = ROOT / 'build/rootfs'
    output = ROOT / 'build/runtime'
    output.mkdir(parents=True, exist_ok=True)
    shutil.copy2(str(ROOT / 'runtime/worldos-init'), str(output / 'worldos-init'))
    shutil.copy2(str(ROOT / 'runtime/input-session.sh'), str(output / 'input-session.sh'))
    for name in ['packages.lock.json', 'sources.lock.json']:
        source = ROOT / 'runtime' / name
        if source.exists():
            shutil.copy2(str(source), str(output / name))
    if not (ROOT / 'build/runtime-installed').exists():
        raise SystemExit('Run make prepare-runtime first')
    kernel = next((filesystem / 'lib/modules').iterdir()).name
    # Some host kmod builds have neither ZLIB nor XZ support. Uncompressed ELF
    # modules also work with the small bootstrap busybox modprobe.
    for compressed in (filesystem / 'lib/modules' / kernel).rglob('*.ko.gz'):
        compressed.with_suffix('').write_bytes(gzip.decompress(compressed.read_bytes()))
        compressed.unlink()
    kernel_link = filesystem / 'lib/modules' / kernel / 'vmlinuz'
    if kernel_link.is_symlink():
        kernel_link.unlink()
        kernel_link.symlink_to('../../../boot/vmlinuz-virt')
    subprocess.run(['depmod', '-b', str(filesystem), kernel], check=True)
    for source, destination in [('worldos-init', 'sbin/worldos-init'), ('xorg.conf', 'etc/X11/xorg.conf')]:
        target = filesystem / destination
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(str(ROOT / 'runtime' / source), str(target))
        if source == 'worldos-init':
            target.chmod(0o755)
    (filesystem / 'etc/hostname').write_text('worldos\n')
    (filesystem / 'etc/apk/repositories').write_text('https://dl-cdn.alpinelinux.org/alpine/v3.24/main\nhttps://dl-cdn.alpinelinux.org/alpine/v3.24/community\n')
    for directory in ['dev', 'proc', 'sys', 'run', 'tmp', 'home/user', 'opt/worldos']:
        (filesystem / directory).mkdir(parents=True, exist_ok=True)
    shutil.copy2(str(filesystem / 'boot/vmlinuz-virt'), str(output / 'vmlinuz'))
    entries = [(directory, stat.S_IFDIR | 0o755, b'', 0, 0) for directory in ['bin', 'sbin', 'dev', 'proc', 'sys', 'run', 'lib', 'lib/modules', 'edition']]
    entries += [('dev/console', stat.S_IFCHR | 0o600, b'', 5, 1),
                ('dev/null', stat.S_IFCHR | 0o666, b'', 1, 3),
                ('bin/busybox', stat.S_IFREG | 0o755, Path('/bin/busybox').read_bytes(), 0, 0),
                ('bin/sh', stat.S_IFLNK | 0o777, b'busybox', 0, 0),
                ('init', stat.S_IFREG | 0o755, (ROOT / 'runtime/init').read_bytes(), 0, 0)]
    for name, mode, data, major, minor in directory_entries(filesystem / 'lib/modules'):
        entries.append(('lib/modules/' + name, mode, data, major, minor))
    cpio(entries, output / 'base.cpio')
    with (output / 'base.cpio').open('rb') as source, (output / 'base.cpio.gz').open('wb') as target:
        with gzip.GzipFile(fileobj=target, mode='wb', compresslevel=1, mtime=0) as compressed:
            shutil.copyfileobj(source, compressed)
    # A new file replaces the previous build only when squashfs creation succeeds.
    if '--bootstrap' not in sys.argv:
        subprocess.run([str(filesystem / 'lib/ld-musl-x86_64.so.1'), '--library-path',
                        str(filesystem / 'lib') + ':' + str(filesystem / 'usr/lib'),
                        str(filesystem / 'usr/bin/glib-compile-schemas'),
                        str(filesystem / 'usr/share/glib-2.0/schemas')], check=True)
        # Build target fontconfig caches without chroot or host installation.
        # --system-only and --sysroot confine cache writes to the guest tree.
        subprocess.run([str(filesystem / 'lib/ld-musl-x86_64.so.1'), '--library-path',
                        str(filesystem / 'lib') + ':' + str(filesystem / 'usr/lib'),
                        str(filesystem / 'usr/bin/fc-cache'), '--system-only', '--sysroot=' + str(filesystem)], check=True)
        temporary = output / 'rootfs.squashfs.next'
        subprocess.run(['mksquashfs', str(filesystem), str(temporary), '-noappend', '-all-root',
                        '-comp', 'gzip', '-processors', '2', '-no-progress'], check=True)
        temporary.replace(output / 'rootfs.squashfs')
    manifest = {'kernel': kernel, 'jdk': 'OpenJDK 25', 'base': 'Alpine 3.24', 'files': {}}
    for name in ['vmlinuz', 'base.cpio.gz', 'rootfs.squashfs', 'worldos-init', 'input-session.sh']:
        path = output / name
        manifest['files'][name] = {'bytes': path.stat().st_size, 'sha256': hashlib.sha256(path.read_bytes()).hexdigest()}
    (output / 'manifest.json').write_text(json.dumps(manifest, indent=2) + '\n')
    print(json.dumps(manifest, indent=2), flush=True)

if __name__ == '__main__':
    main()
