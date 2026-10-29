#!/usr/bin/env python3
"""Boot ARM64 Linux with the same root/initramfs, then migrate its home."""
import argparse
import json
import os
from pathlib import Path
import shutil
import subprocess
import time

from prepare import ROOT, digest
from build import data_image


def boot(stage, data, log, timeout, migrated=None):
    host = ROOT / 'build/host'
    emulator = ['qemu-system-aarch64']
    if (host / 'usr/bin/qemu-system-aarch64').is_file():
        emulator = [str(host / 'lib/ld-musl-x86_64.so.1'), '--library-path',
                    str(host / 'usr/lib') + ':' + str(host / 'lib'),
                    str(host / 'usr/bin/qemu-system-aarch64'), '-L', str(host / 'usr/share/qemu')]
    command = emulator + ['-machine', 'virt', '-cpu', 'cortex-a72',
               '-m', '2048', '-smp', '2', '-display', 'none', '-monitor', 'none',
               '-serial', 'stdio', '-no-reboot', '-kernel', str(ROOT / 'dist/vmlinuz-virt'),
               '-initrd', str(ROOT / 'dist/initramfs-jkoros'), '-append',
               'console=ttyAMA0 jkoros.system=/dev/vda jkoros.data=' +
               ('/dev/vdb' if stage == 'migrate' else 'LABEL=JKDATA') + ' jkoros.test=' + stage,
               '-drive', 'if=none,id=system,format=raw,readonly=on,file=' + str(ROOT / 'dist/system.squashfs'),
               '-device', 'virtio-blk-pci,drive=system,addr=0x2',
               '-drive', 'if=none,id=data,format=raw,file=' + str(data),
               '-device', 'virtio-blk-pci,drive=data,addr=0x3',
               '-netdev', 'user,id=net0', '-device', 'virtio-net-device,netdev=net0']
    if migrated is not None:
        command += ['-drive', 'if=none,id=migrated,format=raw,file=' + str(migrated),
                    '-device', 'virtio-blk-pci,drive=migrated,addr=0x4']
    with log.open('wb') as output:
        process = subprocess.Popen(command, stdout=output, stderr=subprocess.STDOUT)
        try:
            deadline = time.monotonic() + timeout
            while process.poll() is None:
                if time.monotonic() > deadline:
                    raise subprocess.TimeoutExpired(command, timeout)
                text = log.read_text(errors='replace')
                if 'JKOROS BOOT ERROR' in text or 'Kernel panic' in text or 'JKOROS_GUEST_TEST_FAIL' in text:
                    process.terminate()
                    break
                time.sleep(1)
            status = process.wait(timeout=10)
        except subprocess.TimeoutExpired:
            process.terminate()
            try:
                process.wait(timeout=10)
            except subprocess.TimeoutExpired:
                process.kill(); process.wait()
            raise RuntimeError('Boot timed out; see ' + str(log))
    text = log.read_text(errors='replace')
    if status or 'JKOROS_GUEST_TEST_PASS' not in text or 'JKOROS_GUEST_TEST_FAIL' in text:
        raise RuntimeError('Guest test failed; see ' + str(log))
    if stage != 'migrate' and ('JKOROS_OVERLAY_READONLY' not in text or 'JKOROS_DATA_READONLY' not in text):
        raise RuntimeError('Clean read-only shutdown was not confirmed; see ' + str(log))
    return {'stage': stage, 'exit_code': status, 'log': str(log), 'sha256': digest(log)}


def main():
    p = argparse.ArgumentParser()
    p.add_argument('--timeout', type=int, default=900)
    p.add_argument('--stage', choices=['seed', 'restore', 'all'], default='all')
    p.add_argument('--data', type=Path)
    args = p.parse_args()
    report_dir = ROOT / 'build/verification'
    report_dir.mkdir(exist_ok=True)
    data = args.data or report_dir / ('user-' + str(int(time.time())) + '.img')
    if not data.exists():
        data_image(data, 2048)
    results = []
    for stage in (['seed', 'restore'] if args.stage == 'all' else [args.stage]):
        print('ARM64 boot:', stage, flush=True)
        results.append(boot(stage, data, report_dir / (stage + '.log'), args.timeout))
    if args.stage == 'all':
        migrated = data.with_name(data.stem + '-migrated.img')
        data_image(migrated, 2048)
        print('Offline /home/user migration:', flush=True)
        results.append(boot('migrate', data, report_dir / 'migrate.log', args.timeout, migrated))
        results.append(boot('restore', migrated, report_dir / 'migrated-restore.log', args.timeout))
    report = {'hardware_tested': False, 'machine': 'QEMU virt, ARM64 TCG',
              'base_id': json.loads((ROOT / 'dist/manifest.json').read_text())['base_id'],
              'data_image': str(data), 'results': results}
    (report_dir / 'boot.json').write_text(json.dumps(report, indent=2) + '\n')
    print(json.dumps(report, indent=2), flush=True)


if __name__ == '__main__':
    main()
