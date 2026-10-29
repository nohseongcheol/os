#!/usr/bin/env python3
"""명시한 Java извор_стабло/класа_вриједност 파일을 부팅 시 RAM 파일체계로 가져온다."""
import argparse
from pathlib import Path
import re
import struct


def повезати_крајња_тачка(항목들):
    파일들 = []
    이름들 = {'Hello.java'}
    명시 = set()
    for унос_вриједност in 항목들:
        if '=' not in унос_вриједност:
            raise ValueError('expected NAME=PATH: ' + унос_вриједност)
        Назив, ПУТАЊА = унос_вриједност.split('=', 1)
        if not re.fullmatch(r'[A-Za-z0-9_-][A-Za-z0-9_.-]{0,62}', Назив) or Назив in 명시:
            raise ValueError('invalid or duplicate file name: ' + Назив)
        명시.add(Назив)
        이름들.add(Назив)
        подаци = Path(ПУТАЊА).read_bytes()
        if len(подаци) > 16384:
            raise ValueError('file exceeds 16384 bytes: ' + Назив)
        파일들.append((Назив.encode('ascii'), подаци))
    if len(이름들) > 8:
        raise ValueError('RAM file limit: 8 files including the default Hello.java')
    ИСХОД = bytearray(struct.pack('<4sI', b'JKJF', len(파일들)))
    ИСХОД.extend(bytes(72 * len(파일들)))
    for 수, (Назив, подаци) in enumerate(파일들):
        struct.pack_into('<64sII', ИСХОД, 8 + 수 * 72, Назив, len(ИСХОД), len(подаци))
        ИСХОД.extend(подаци)
    return bytes(ИСХОД)


if __name__ == '__main__':
    рашчланити_вриједност = argparse.ArgumentParser(description=__doc__)
    рашчланити_вриједност.add_argument('-o', required=True)
    рашчланити_вриједност.add_argument('files', nargs='*', help='NAME=PATH')
    Аргументи = рашчланити_вриједност.parse_args()
    try:
        подаци = повезати_крајња_тачка(Аргументи.files)
        одредиште_вриједност = Path(Аргументи.o)
        if not одредиште_вриједност.exists() or одредиште_вриједност.read_bytes() != подаци:
            임시 = одредиште_вриједност.with_name(одредиште_вриједност.name + '.tmp')
            임시.write_bytes(подаци)
            임시.replace(одредиште_вриједност)
    except (ValueError, OSError) as ГРЕШКА:
        рашчланити_вриједност.error(str(ГРЕШКА))
