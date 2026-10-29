#!/usr/bin/env python3
"""명시한 Java източник_дърво/Клас_стойност 파일을 부팅 시 RAM 파일체계로 가져온다."""
import argparse
from pathlib import Path
import re
import struct


def обвързвам_участник(항목들):
    파일들 = []
    이름들 = {'Hello.java'}
    명시 = set()
    for запис_стойност in 항목들:
        if '=' not in запис_стойност:
            raise ValueError('expected NAME=PATH: ' + запис_стойност)
        Име, ПЪТ = запис_стойност.split('=', 1)
        if not re.fullmatch(r'[A-Za-z0-9_-][A-Za-z0-9_.-]{0,62}', Име) or Име in 명시:
            raise ValueError('invalid or duplicate file name: ' + Име)
        명시.add(Име)
        이름들.add(Име)
        данни = Path(ПЪТ).read_bytes()
        if len(данни) > 16384:
            raise ValueError('file exceeds 16384 bytes: ' + Име)
        파일들.append((Име.encode('ascii'), данни))
    if len(이름들) > 8:
        raise ValueError('RAM file limit: 8 files including the default Hello.java')
    РЕЗУЛТАТ = bytearray(struct.pack('<4sI', b'JKJF', len(파일들)))
    РЕЗУЛТАТ.extend(bytes(72 * len(파일들)))
    for 수, (Име, данни) in enumerate(파일들):
        struct.pack_into('<64sII', РЕЗУЛТАТ, 8 + 수 * 72, Име, len(РЕЗУЛТАТ), len(данни))
        РЕЗУЛТАТ.extend(данни)
    return bytes(РЕЗУЛТАТ)


if __name__ == '__main__':
    анализирам_стойност = argparse.ArgumentParser(description=__doc__)
    анализирам_стойност.add_argument('-o', required=True)
    анализирам_стойност.add_argument('files', nargs='*', help='NAME=PATH')
    Параметри = анализирам_стойност.parse_args()
    try:
        данни = обвързвам_участник(Параметри.files)
        местоназначение_стойност = Path(Параметри.o)
        if not местоназначение_стойност.exists() or местоназначение_стойност.read_bytes() != данни:
            임시 = местоназначение_стойност.with_name(местоназначение_стойност.name + '.tmp')
            임시.write_bytes(данни)
            임시.replace(местоназначение_стойност)
    except (ValueError, OSError) as ГРЕШКА:
        анализирам_стойност.error(str(ГРЕШКА))
