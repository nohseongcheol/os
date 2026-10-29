#!/usr/bin/env python3
"""Build regular image files only. No root, loop mounts or physical disks."""
import argparse
import gzip
import hashlib
import json
import lzma
import os
from pathlib import Path
import shutil
import stat
import struct
import subprocess
import tarfile
import time

from archive import write_cpio
from prepare import ROOT, RELEASE, digest

PROJECT = ROOT.parents[1]
FILESYSTEM = ROOT / 'build/rootfs'
DIST = ROOT / 'dist'


def kernel_image(source, destination):
    data = Path(source).read_bytes()
    # Alpine's generic ARM64 kernel is an EFI zboot executable. Direct QEMU
    # boot and Raspberry Pi firmware require the contained Linux Image.
    if data[4:8] == b'zimg':
        offset, length = struct.unpack_from('<II', data, 8)
        if offset + length > len(data) or data[24:28] != b'gzip':
            raise ValueError('Unsupported EFI zboot format: ' + str(source))
        data = gzip.decompress(data[offset:offset + length])
    elif data[:2] == b'\x1f\x8b':
        data = gzip.decompress(data)
    if data[56:60] != b'ARM\x64':
        raise ValueError('Not a Linux ARM64 Image: ' + str(source))
    Path(destination).write_bytes(data)


def run(*args):
    subprocess.run([str(x) for x in args], check=True)


def put(path, text, mode=0o644):
    path = FILESYSTEM / path
    path.parent.mkdir(parents=True, exist_ok=True)
    if path.exists():
        path.chmod(path.stat().st_mode | stat.S_IWUSR)
    path.write_text(text)
    path.chmod(mode)


def copy(source, destination, mode=None):
    destination = FILESYSTEM / destination
    destination.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(str(source), str(destination))
    if mode is not None:
        destination.chmod(mode)


def configure():
    for name in ['dev', 'proc', 'sys', 'run', 'tmp', 'home/user', 'opt/jkoros/lib', 'etc/skel/workspace']:
        (FILESYSTEM / name).mkdir(parents=True, exist_ok=True)
    for source, dest in [('rc', 'usr/local/sbin/jkoros-rc'), ('shutdown', 'usr/local/sbin/jkoros-shutdown'),
                         ('desktop', 'usr/local/bin/jkoros-desktop'), ('session', 'usr/local/bin/jkoros-session'),
                         ('environment', 'usr/local/bin/jkoros-environment')]:
        copy(ROOT / 'runtime' / source, dest, 0o755)
    copy(ROOT / 'runtime/profile', 'etc/profile.d/jkoros.sh')
    copy(ROOT / 'runtime/terminal', 'usr/local/bin/jkoros-terminal', 0o755)
    copy(ROOT / 'runtime/desktop-settings.py', 'usr/local/lib/jkoros/desktop-settings.py', 0o755)
    copy(ROOT / 'runtime/fonts.conf', 'etc/fonts/conf.d/60-jkoros-desktop.conf')
    copy(ROOT / 'runtime/Xresources', 'etc/jkoros/Xresources')
    for alias in ['default-jvm', 'default-jre']:
        path = FILESYSTEM / 'usr/lib/jvm' / alias
        if path.is_symlink():
            path.unlink()
        if not path.exists():
            path.symlink_to('java-25-openjdk')
    # APK post-install scripts are intentionally not run on the build host.
    # Recreate the JDK alternatives explicitly instead.
    for program in (FILESYSTEM / 'usr/lib/jvm/java-25-openjdk/bin').iterdir():
        link = FILESYSTEM / 'usr/bin' / program.name
        if not link.exists() and not link.is_symlink():
            link.symlink_to('../lib/jvm/default-jvm/bin/' + program.name)
    if (ROOT / 'build/jre-aarch64/bin/java').exists():
        target = FILESYSTEM / 'usr/lib/jvm/java-25-jre'
        if target.exists():
            shutil.rmtree(str(target))
        shutil.copytree(str(ROOT / 'build/jre-aarch64'), str(target), symlinks=True)
    put('etc/inittab', '::sysinit:/usr/local/sbin/jkoros-rc\n'
        'ttyAMA0::respawn:/sbin/getty -n -l /usr/local/bin/jkoros-login 115200 ttyAMA0\n'
        'tty2::respawn:/sbin/getty -n -l /usr/local/bin/jkoros-login 38400 tty2\n'
        '::ctrlaltdel:/sbin/reboot\n::shutdown:/usr/local/sbin/jkoros-shutdown\n')
    put('usr/local/bin/jkoros-login', '#!/bin/sh\nexec /bin/su - user\n', 0o755)
    put('etc/sudoers.d/jkoros', 'user ALL=(ALL) NOPASSWD: ALL\n', 0o440)
    # apk --usermode strips setuid; restore only sudo in the all-root image.
    (FILESYSTEM / 'usr/bin/sudo').chmod(0o4755)
    put('etc/apk/repositories', 'https://dl-cdn.alpinelinux.org/alpine/v3.24/main\n'
        'https://dl-cdn.alpinelinux.org/alpine/v3.24/community\n')
    (FILESYSTEM / 'etc/apk/keys').mkdir(parents=True, exist_ok=True)
    for key in (ROOT / 'build/bootstrap/keys').iterdir():
        copy(key, 'etc/apk/keys/' + key.name)
    put('etc/hostname', 'jkoros\n')
    put('etc/jkoros-build-epoch', str(int(time.time())) + '\n')
    put('etc/skel/.profile', '. /etc/profile.d/jkoros.sh\n')
    put('etc/skel/.bash_profile', '. /etc/profile\n')
    put('etc/skel/.config/fcitx5/profile', '[Groups/0]\nName=Default\nDefault Layout=us\nDefaultIM=hangul\n\n'
        '[Groups/0/Items/0]\nName=keyboard-us\nLayout=\n\n[Groups/0/Items/1]\nName=hangul\nLayout=\n\n[GroupOrder]\n0=Default\n')
    put('etc/skel/.config/jkoros/README', 'Wi-Fi: save wpa_supplicant configuration as wifi.conf, chmod 600.\n')
    copy(FILESYSTEM / 'etc/xdg/openbox/rc.xml', 'etc/skel/.config/openbox/rc.xml')
    for name in ['sh', 'mount', 'umount', 'mkdir', 'cat', 'chmod', 'chown', 'sleep', 'sync', 'su']:
        target = FILESYSTEM / 'bin' / name
        if not target.exists() and not target.is_symlink():
            target.symlink_to('busybox')
    for name in ['init', 'getty', 'poweroff', 'reboot']:
        target = FILESYSTEM / 'sbin' / name
        if not target.exists() and not target.is_symlink():
            target.symlink_to('../bin/busybox')
    run('make', '-C', PROJECT / 'स्वकीय_जावा')
    copy(PROJECT / 'स्वकीय_जावा/build/स्वकीय_जावा.jar', 'opt/jkoros/lib/स्वकीय_जावा.jar')
    examples = PROJECT / 'स्वकीय_जावा/उदाहरणे'
    for source in examples.rglob('*'):
        if source.is_file():
            copy(source, Path('etc/skel/workspace') / source.relative_to(examples))
    for source in (PROJECT / 'compiler').iterdir():
        if source.suffix in ('.py', '.s', '.c', '.ld', '.md'):
            copy(source, 'opt/jkoros/compiler/' + source.name)
    put('usr/local/bin/jclassc', '#!/bin/sh\nexec python3 /opt/jkoros/compiler/संकलक.py "$@"\n', 0o755)
    for source in (ROOT / 'tests').iterdir():
        if source.is_file():
            copy(source, 'opt/jkoros/tests/' + source.name, 0o755 if source.suffix == '.sh' else 0o644)
    # Compile test classes with the host JDK; Java 11 bytecode runs on JDK 25.
    java_tests = list((ROOT / 'tests').glob('*.java'))
    if java_tests:
        run('javac', '--release', '11', '-encoding', 'UTF-8', '-cp', FILESYSTEM / 'opt/jkoros/lib/स्वकीय_जावा.jar',
            '-d', FILESYSTEM / 'opt/jkoros/tests', *java_tests)
    test_packages = ROOT / 'vendor/test-packages'
    if test_packages.exists():
        for p in test_packages.glob('*.apk'):
            copy(p, 'opt/jkoros/tests/packages/' + p.name)
    for name in ['packages.lock.json', 'sources.lock.json']:
        copy(ROOT / 'build' / name, 'opt/jkoros/' + name)
    h = hashlib.sha256((ROOT / 'build/packages.lock.json').read_bytes())
    for folder in [ROOT / 'runtime', ROOT / 'tools', PROJECT / 'compiler', PROJECT / 'स्वकीय_जावा/स्रोत']:
        for source in sorted(folder.rglob('*')):
            if source.is_file() and source.suffix in ('.py', '.c', '.s', '.java', '.ld') or source.is_file() and folder == ROOT / 'runtime':
                h.update(str(source.relative_to(PROJECT)).encode())
                h.update(source.read_bytes())
    put('etc/jkoros-base-id', 'jkoros-rpi4-aarch64-' + h.hexdigest()[:24] + '\n')
    return (FILESYSTEM / 'etc/jkoros-base-id').read_text().strip()


def modules():
    versions = sorted(p.name for p in (FILESYSTEM / 'lib/modules').iterdir())
    for version in versions:
        tree = FILESYSTEM / 'lib/modules' / version
        link = tree / 'vmlinuz'
        if link.is_symlink():
            link.unlink()
            link.symlink_to('../../../boot/vmlinuz-' + version.rsplit('-', 1)[-1])
        for compressed in list(tree.rglob('*.ko.gz')) + list(tree.rglob('*.ko.xz')):
            decode = gzip.decompress if compressed.suffix == '.gz' else lzma.decompress
            compressed.with_suffix('').write_bytes(decode(compressed.read_bytes()))
            compressed.unlink()
        run('depmod', '-b', FILESYSTEM, version)
    return versions


def initramfs(versions):
    entries = {}
    def add(name, mode, data=b'', major=0, minor=0):
        parent = str(Path(name).parent)
        if parent != '.' and parent not in entries:
            add(parent, stat.S_IFDIR | 0o755)
        entries[name] = (name, mode, data, major, minor)
    for directory in ['bin', 'sbin', 'dev', 'proc', 'sys', 'run', 'lib/modules']:
        add(directory, stat.S_IFDIR | 0o755)
    add('dev/console', stat.S_IFCHR | 0o600, major=5, minor=1)
    add('dev/null', stat.S_IFCHR | 0o666, major=1, minor=3)
    add('bin/busybox', stat.S_IFREG | 0o755, (FILESYSTEM / 'bin/busybox.static').read_bytes())
    add('bin/sh', stat.S_IFLNK | 0o777, b'busybox')
    add('init', stat.S_IFREG | 0o755, (ROOT / 'runtime/init').read_bytes())
    required = 'loop squashfs overlay ext4 virtio_pci virtio_mmio virtio_blk sdhci sdhci_pltfm sdhci_iproc mmc_block bcm2835 pcie_brcmstb xhci_pci xhci_plat_hcd usb_storage uas'.split()
    for version in versions:
        tree = FILESYSTEM / 'lib/modules' / version
        files = set(p for p in tree.glob('modules.*') if p.is_file())
        for name in required:
            result = subprocess.run(['modprobe', '-d', str(FILESYSTEM), '-S', version, '--show-depends', name],
                                    stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
            for line in result.stdout.splitlines():
                if line.startswith('insmod '):
                    files.add(Path(line.split()[1]))
        for path in sorted(files):
            if path.is_file():
                add(str(path.relative_to(FILESYSTEM)), stat.S_IFREG | 0o644, path.read_bytes())
    write_cpio(entries.values(), ROOT / 'build/initramfs.cpio')
    with (ROOT / 'build/initramfs.cpio').open('rb') as src, (DIST / 'initramfs-jkoros').open('wb') as dst:
        with gzip.GzipFile(fileobj=dst, mode='wb', mtime=0, compresslevel=6) as compressor:
            shutil.copyfileobj(src, compressor)


def boot_image():
    boot = ROOT / 'build/boot'
    boot.mkdir(exist_ok=True)
    # Only regular firmware/DTB files from the checked release are copied.
    with tarfile.open(str(ROOT / 'vendor' / ('alpine-rpi-' + RELEASE + '-aarch64.tar.gz'))) as archive:
        for member in archive:
            name = member.name.lstrip('./')
            if not member.isfile() or '/' in name or name.endswith(('.txt', '.dtb')) or name.startswith('.'):
                continue
            (boot / name).write_bytes(archive.extractfile(member).read())
    for source in (FILESYSTEM / 'boot').glob('*.dtb'):
        shutil.copy2(str(source), str(boot / source.name))
    shutil.copytree(str(FILESYSTEM / 'boot/overlays'), str(boot / 'overlays')) if not (boot / 'overlays').exists() else None
    kernel_image(FILESYSTEM / 'boot/vmlinuz-rpi', boot / 'kernel8.img')
    shutil.copy2(str(DIST / 'initramfs-jkoros'), str(boot / 'initramfs-jkoros'))
    (boot / 'config.txt').write_text('arm_64bit=1\nkernel=kernel8.img\ninitramfs initramfs-jkoros followkernel\n'
        'enable_uart=1\ndtoverlay=disable-bt\ndtoverlay=vc4-kms-v3d\nmax_framebuffers=2\n'
        'dtparam=audio=on\ndisable_overscan=1\n')
    (boot / 'cmdline.txt').write_text('console=serial0,115200 console=tty1 jkoros.system=/dev/mmcblk0p2 jkoros.data=LABEL=JKDATA\n')
    image = ROOT / 'build/boot.fat'
    with image.open('wb') as f:
        f.truncate(256 * 1024 * 1024)
    run('mkfs.vfat', '-F', '32', '-n', 'JKBOOT', image)
    run('mcopy', '-i', image, '-s', *sorted(boot.iterdir()), '::/')
    return image


def disk_image(boot, system):
    start1 = 2048
    size1 = boot.stat().st_size // 512
    start2 = start1 + size1
    size2 = (system.stat().st_size + 511) // 512
    mbr = bytearray(512)
    struct.pack_into('<I', mbr, 440, 0x4a4b4f53)
    for i, (start, size, kind) in enumerate([(start1, size1, 0x0c), (start2, size2, 0x83)]):
        struct.pack_into('<B3sB3sII', mbr, 446 + i * 16, 0, b'\xfe\xff\xff', kind, b'\xfe\xff\xff', start, size)
    mbr[510:] = b'\x55\xaa'
    result = DIST / 'jkoros-rpi4-system.img'
    with result.open('wb') as f:
        f.truncate((start2 + size2 + 2048) * 512)
        f.seek(0); f.write(mbr)
        for start, source in [(start1, boot), (start2, system)]:
            f.seek(start * 512)
            with source.open('rb') as src:
                shutil.copyfileobj(src, f)
    return result


def data_image(path, size_mib):
    path = Path(path)
    if path.exists():
        raise SystemExit('Refusing to overwrite user data: ' + str(path))
    with path.open('xb') as f:
        f.truncate(size_mib * 1024 * 1024)
    run('mke2fs', '-q', '-t', 'ext4', '-F', '-L', 'JKDATA', '-m', '0', path)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--data-only', type=Path)
    parser.add_argument('--data-mib', type=int, default=4096)
    args = parser.parse_args()
    DIST.mkdir(exist_ok=True)
    if args.data_only:
        data_image(args.data_only, args.data_mib)
        return
    if not (ROOT / 'build/prepared').is_file():
        raise SystemExit('Run tools/prepare.py first')
    base_id = configure()
    versions = modules()
    initramfs(versions)
    run('mksquashfs', FILESYSTEM, DIST / 'system.squashfs', '-noappend', '-all-root',
        '-comp', 'gzip', '-Xcompression-level', '1', '-processors', '2', '-no-progress')
    kernel_image(FILESYSTEM / 'boot/vmlinuz-virt', DIST / 'vmlinuz-virt')
    boot = boot_image()
    image = disk_image(boot, DIST / 'system.squashfs')
    if not (DIST / 'jkoros-user.img').exists():
        data_image(DIST / 'jkoros-user.img', args.data_mib)
    manifest = {'base_id': base_id, 'arch': 'aarch64', 'board': 'Raspberry Pi 4',
                'kernels': versions, 'boot_hardware_tested': False,
                'user_data': 'Separate ext4 disk JKDATA; /user maps to /home/user',
                'files': {}}
    for name in [image.name, 'system.squashfs', 'initramfs-jkoros', 'vmlinuz-virt']:
        p = DIST / name
        manifest['files'][name] = {'bytes': p.stat().st_size, 'sha256': digest(p)}
    (DIST / 'manifest.json').write_text(json.dumps(manifest, indent=2) + '\n')
    for name in ['packages.lock.json', 'sources.lock.json']:
        shutil.copy2(str(ROOT / 'build' / name), str(DIST / name))
    shutil.copy2(str(PROJECT / 'स्वकीय_जावा/build/स्वकीय_जावा.jar'), str(DIST / 'स्वकीय_जावा.jar'))
    print(json.dumps(manifest, indent=2), flush=True)


if __name__ == '__main__':
    main()
