#!/usr/bin/env python3
"""Verify distributed bytes independently of the image-building code."""
import gzip
import hashlib
import json
import struct
import subprocess
import tarfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DIST = ROOT / 'dist'


def sha256(path):
    h = hashlib.sha256()
    with Path(path).open('rb') as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b''):
            h.update(block)
    return h.hexdigest()


def main():
    report = {}
    manifest = json.loads((DIST / 'manifest.json').read_text())
    for name, metadata in manifest['files'].items():
        path = DIST / name
        assert path.stat().st_size == metadata['bytes'], name
        assert sha256(path) == metadata['sha256'], name
    image = DIST / 'jkoros-rpi4-system.img'
    with image.open('rb') as disk:
        mbr = disk.read(512)
        assert mbr[510:512] == b'\x55\xaa'
        parts = [struct.unpack_from('<B3sB3sII', mbr, 446 + 16 * i) for i in range(2)]
        first, second = parts
        assert first[2] == 0x0c and second[2] == 0x83
        assert first[4] >= 2048 and first[4] + first[5] <= second[4]
        assert (second[4] + second[5]) * 512 <= image.stat().st_size
        disk.seek(second[4] * 512)
        assert disk.read(4) == b'hsqs'
    fat = str(image) + '@@' + str(first[4] * 512)
    def read_fat(name):
        return subprocess.check_output(['mtype', '-i', fat, '::/' + name])
    config = read_fat('config.txt').decode()
    command = read_fat('cmdline.txt').decode()
    assert 'kernel=kernel8.img' in config and 'arm_64bit=1' in config
    assert 'initramfs initramfs-jkoros followkernel' in config
    assert 'jkoros.data=LABEL=JKDATA' in command and '/dev/mmcblk0p2' in command
    assert read_fat('kernel8.img')[56:60] == b'ARM\x64'
    assert read_fat('bcm2711-rpi-4-b.dtb')[:4] == b'\xd0\x0d\xfe\xed'
    assert len(read_fat('start4.elf')) > 100000
    assert gzip.decompress(read_fat('initramfs-jkoros')).startswith(b'070701')
    report['partition_table_firmware_arm64_kernel_device_tree_initramfs'] = 'pass'
    java = json.loads((DIST / 'java-runtimes.json').read_text())
    for record in java:
        path = DIST / record['file']
        assert sha256(path) == record['sha256']
        with tarfile.open(str(path)) as archive:
            entry = next(m for m in archive if m.name.endswith('/bin/java') and m.isfile())
            header = archive.extractfile(entry).read(64)
            assert header[:4] == b'\x7fELF' and struct.unpack_from('<H', header, 18)[0] == 183
    report['arm64_jdk_jre_and_checksums'] = 'pass'
    report['base_id'] = manifest['base_id']
    report['raspberry_pi_hardware_tested'] = False
    output = ROOT / 'build/verification/image.json'
    output.parent.mkdir(exist_ok=True)
    output.write_text(json.dumps(report, indent=2) + '\n')
    print(json.dumps(report, indent=2))


if __name__ == '__main__':
    main()
