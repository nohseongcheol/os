"""Write newc initramfs records with deterministic root ownership."""
from pathlib import Path


def write_cpio(entries, output):
    with Path(output).open('wb') as stream:
        for inode, (name, mode, data, major, minor) in enumerate(
                list(entries) + [('TRAILER!!!', 0, b'', 0, 0)], 1):
            raw = name.encode('utf-8') + b'\0'
            fields = [inode, mode, 0, 0, 1, 0, len(data), 0, 0, major, minor, len(raw), 0]
            stream.write(b'070701' + b''.join(('%08x' % x).encode() for x in fields))
            stream.write(raw)
            stream.write(b'\0' * (-(110 + len(raw)) % 4))
            stream.write(data)
            stream.write(b'\0' * (-len(data) % 4))
