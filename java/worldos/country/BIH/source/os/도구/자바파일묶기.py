#!/usr/bin/env python3
"""명시한 Java извор_стабло/класа_вриједност 파일을 부팅 시 RAM 파일체계로 가져온다."""
import argparse
from pathlib import Path
import re
import struct


def повезати_крајња_тачка_bbe6b410(항목들):
    파일들 = []
    이름들 = {'Hello.java'}
    명시 = set()
    for унос_вриједност in 항목들:
        if '=' not in унос_вриједност:
            raise ValueError('expected NAME=PATH: ' + унос_вриједност)
        назив, пут = унос_вриједност.split('=', 1)
        if not re.fullmatch(r'[A-Za-z0-9_-][A-Za-z0-9_.-]{0,62}', назив) or назив in 명시:
            raise ValueError('invalid or duplicate file name: ' + назив)
        명시.add(назив)
        이름들.add(назив)
        подаци = Path(пут).read_bytes()
        if len(подаци) > 16384:
            raise ValueError('file exceeds 16384 bytes: ' + назив)
        파일들.append((назив.encode('ascii'), подаци))
    if len(이름들) > 8:
        raise ValueError('RAM file limit: 8 files including the default Hello.java')
    결과 = bytearray(struct.pack('<4sI', b'JKJF', len(파일들)))
    결과.extend(bytes(72 * len(파일들)))
    for 수, (назив, подаци) in enumerate(파일들):
        struct.pack_into('<64sII', 결과, 8 + 수 * 72, назив, len(결과), len(подаци))
        결과.extend(подаци)
    return bytes(결과)


if __name__ == '__main__':
    рашчлањивати_вриједност = argparse.ArgumentParser(description=__doc__)
    рашчлањивати_вриједност.add_argument('-o', required=True)
    рашчлањивати_вриједност.add_argument('files', nargs='*', help='NAME=PATH')
    인수 = рашчлањивати_вриједност.parse_args()
    try:
        подаци = повезати_крајња_тачка_bbe6b410(인수.files)
        одредиште_вриједност = Path(인수.o)
        if not одредиште_вриједност.exists() or одредиште_вриједност.read_bytes() != подаци:
            임시 = одредиште_вриједност.with_name(одредиште_вриједност.name + '.tmp')
            임시.write_bytes(подаци)
            임시.replace(одредиште_вриједност)
    except (ValueError, OSError) as грешка:
        рашчлањивати_вриједност.error(str(грешка))
