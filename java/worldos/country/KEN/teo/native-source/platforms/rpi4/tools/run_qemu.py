#!/usr/bin/env python3
"""Run the existing ARM64 image with a local VNC desktop or serial console."""
import argparse
import gzip
import hashlib
import os
from pathlib import Path
import tempfile

from prepare import ROOT
from build import data_image
from archive import write_cpio
from desktop_update import payload


def graphical_initramfs():
    """Preload guest display/input drivers without changing the installed base.

    Older images trigger udev with its default 'change' action, so the 'add'
    driver-loading rule is skipped. Load from the real root just before init.
    This keeps existing user images compatible with their original base-id.
    """
    source = (ROOT / 'dist/initramfs-jkoros').read_bytes()
    raw = gzip.decompress(source)
    entries = []
    position = 0
    patched = False
    update = payload()
    hook = (b'for module in bochs usbhid hid_generic evdev; do\n'
            b'    /bin/busybox chroot /newroot /sbin/modprobe "$module" || fail "QEMU driver: $module"\n'
            b'done\n'
            b'mkdir -p /newroot/run/jkoros/desktop-update\n'
            b'cp -a /desktop-update/. /newroot/run/jkoros/desktop-update/\n'
            b'/bin/busybox chroot /newroot /usr/bin/python3 /run/jkoros/desktop-update/apply.py || fail "Desktop update"\n')
    while position + 110 <= len(raw):
        if raw[position:position + 6] != b'070701':
            raise RuntimeError('Unsupported initramfs format; expected newc')
        fields = [int(raw[position + 6 + i * 8:position + 14 + i * 8], 16) for i in range(13)]
        name_end = position + 110 + fields[11]
        name = raw[position + 110:name_end - 1].decode('utf-8')
        start = (name_end + 3) & ~3
        data = raw[start:start + fields[6]]
        position = (start + fields[6] + 3) & ~3
        if name == 'TRAILER!!!':
            break
        if name == 'init':
            marker = b'exec switch_root /newroot /sbin/init'
            if data.count(marker) != 1:
                raise RuntimeError('Cannot locate the graphical boot hook in initramfs')
            data = data.replace(marker, hook + marker)
            patched = True
        entries.append((name, fields[1], data, fields[9], fields[10]))
    if not patched:
        raise RuntimeError('init was not found in initramfs')
    directories = set()
    for name, (mode, data) in sorted(update.items()):
        destination = 'desktop-update/' + name
        for parent in reversed(Path(destination).parents):
            if str(parent) != '.' and str(parent) not in directories:
                entries.append((str(parent), 0o040755, b'', 0, 0))
                directories.add(str(parent))
        entries.append((destination, 0o100000 | mode, data, 0, 0))
    stamp = hashlib.sha256(source + hook + update['manifest.json'][1]).hexdigest()[:20]
    output = ROOT / 'build' / ('initramfs-qemu-' + stamp + '.gz')
    if not output.exists():
        with tempfile.TemporaryDirectory(prefix='qemu-init-', dir=str(ROOT / 'build')) as tmp:
            cpio = Path(tmp) / 'initramfs.cpio'
            write_cpio(entries, cpio)
            packed = Path(tmp) / 'initramfs.gz'
            with packed.open('wb') as stream:
                with gzip.GzipFile(fileobj=stream, mode='wb', mtime=0) as compressed:
                    compressed.write(cpio.read_bytes())
            packed.replace(output)
    return output


def command(data, graphical=True, vnc_port=5901, monitor=None):
    host = ROOT / 'build/host'
    emulator = [str(host / 'lib/ld-musl-x86_64.so.1'), '--library-path',
                str(host / 'usr/lib') + ':' + str(host / 'lib'),
                str(host / 'usr/bin/qemu-system-aarch64'),
                '-L', str(host / 'usr/share/qemu')]
    cmdline = 'console=ttyAMA0 jkoros.system=/dev/vda jkoros.data=LABEL=JKDATA'
    if not graphical:
        cmdline += ' jkoros.desktop=off'
    result = emulator + ['-machine', 'virt', '-accel', 'tcg', '-cpu', 'cortex-a72',
                         '-m', '2048', '-smp', '2', '-display', 'none',
                         '-monitor', monitor or 'none', '-serial', 'stdio', '-no-reboot',
                         '-kernel', str(ROOT / 'dist/vmlinuz-virt'),
                         '-initrd', str(graphical_initramfs() if graphical else ROOT / 'dist/initramfs-jkoros'), '-append', cmdline,
                         '-drive', 'if=none,id=system,format=raw,readonly=on,file=' + str(ROOT / 'dist/system.squashfs'),
                         '-device', 'virtio-blk-pci,drive=system,addr=0x2',
                         '-drive', 'if=none,id=data,format=raw,file=' + str(data),
                         '-device', 'virtio-blk-pci,drive=data,addr=0x3',
                         '-netdev', 'user,id=net0', '-device', 'virtio-net-device,netdev=net0']
    if graphical:
        # Both QEMU's bochs-display and the guest's bochs DRM driver are already
        # included. VNC does not require a host GTK/SDL module or guest Xvfb.
        result += ['-device', 'bochs-display', '-device', 'qemu-xhci',
                   '-device', 'usb-kbd', '-device', 'usb-tablet',
                   '-vnc', '127.0.0.1:' + str(vnc_port - 5900)]
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--console', action='store_true', help='disable the graphical desktop')
    parser.add_argument('--data', type=Path, default=ROOT / 'build/manual-user.img')
    parser.add_argument('--vnc-port', type=int, default=5901)
    args = parser.parse_args()
    if not 5900 <= args.vnc_port <= 65535:
        parser.error('--vnc-port must be between 5900 and 65535')
    for name in ['vmlinuz-virt', 'initramfs-jkoros', 'system.squashfs']:
        if not (ROOT / 'dist' / name).is_file():
            parser.error('Missing dist/' + name + '; run make image first')
    if not (ROOT / 'build/host/usr/bin/qemu-system-aarch64').is_file():
        parser.error('QEMU is missing; run make prepare-host first')
    data = args.data.expanduser().resolve()
    if not data.exists():
        data_image(data, 2048)
    if not data.is_file():
        parser.error('Data image must be a regular file: ' + str(data))
    print('User data image:', data, flush=True)
    if not args.console:
        profile = ROOT / 'build' / ('qemu-' + str(args.vnc_port) + '.remmina')
        profile.write_text('[remmina]\nname=jkoros QEMU desktop\nprotocol=VNC\n'
                           'server=127.0.0.1:' + str(args.vnc_port) + '\ncolordepth=32\nviewmode=1\n')
        print('VNC desktop: 127.0.0.1:' + str(args.vnc_port), flush=True)
        print('On the host, open Remmina with: remmina -c ' + str(profile), flush=True)
        print('Run Swing programs in the desktop terminal. Shut down with sudo poweroff.', flush=True)
    argv = command(data, not args.console, args.vnc_port)
    os.execv(argv[0], argv)


if __name__ == '__main__':
    main()
