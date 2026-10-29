"""Deterministic newc initramfs writer; no mount, mknod, or root needed."""
import os
from pathlib import Path
import stat

def cpio(entries, output):
    inode = 1
    with Path(output).open('wb') as stream:
        for name, mode, data, major, minor in list(entries) + [('TRAILER!!!', 0, b'', 0, 0)]:
            raw_name = name.encode('utf-8') + b'\0'
            values = [inode, mode, 0, 0, 1, 0, len(data), 0, 0, major, minor, len(raw_name), 0]
            stream.write(b'070701' + b''.join(('%08x' % value).encode() for value in values))
            stream.write(raw_name)
            stream.write(b'\0' * (-(110 + len(raw_name)) % 4))
            stream.write(data)
            stream.write(b'\0' * (-len(data) % 4))
            inode += 1

def directory_entries(root):
    root = Path(root)
    for path in sorted(root.rglob('*')):
        info = path.lstat()
        mode = info.st_mode
        if path.is_symlink():
            data = os.readlink(str(path)).encode()
        elif stat.S_ISREG(mode):
            data = path.read_bytes()
        elif stat.S_ISDIR(mode):
            data = b''
        else:
            raise ValueError('Unsupported host filesystem node: ' + str(path))
        yield str(path.relative_to(root)), mode, data, 0, 0
