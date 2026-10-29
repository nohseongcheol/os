#!/usr/bin/env python3
"""명시한 Java джерело_дерево/Клас_значення 파일을 запуск_машини 시 RAM 파일체계로 가져온다."""
import argparse
from pathlib import Path
import re
import struct


def зв_язувати_учасник(항목들):
    파일들 = []
    이름들 = {'Hello.java'}
    명시 = set()
    for запис_значення_962f286b in 항목들:
        if '=' not in запис_значення_962f286b:
            raise ValueError('expected NAME=PATH: ' + запис_значення_962f286b)
        Назва, шлях = запис_значення_962f286b.split('=', 1)
        if not re.fullmatch(r'[A-Za-z0-9_-][A-Za-z0-9_.-]{0,62}', Назва) or Назва in 명시:
            raise ValueError('invalid or duplicate file name: ' + Назва)
        명시.add(Назва)
        이름들.add(Назва)
        дані = Path(шлях).read_bytes()
        if len(дані) > 16384:
            raise ValueError('file exceeds 16384 bytes: ' + Назва)
        파일들.append((Назва.encode('ascii'), дані))
    if len(이름들) > 8:
        raise ValueError('RAM file limit: 8 files including the default Hello.java')
    результат = bytearray(struct.pack('<4sI', b'JKJF', len(파일들)))
    результат.extend(bytes(72 * len(파일들)))
    for 수, (Назва, дані) in enumerate(파일들):
        struct.pack_into('<64sII', результат, 8 + 수 * 72, Назва, len(результат), len(дані))
        результат.extend(дані)
    return bytes(результат)


if __name__ == '__main__':
    аналізувати_значення = argparse.ArgumentParser(description=__doc__)
    аналізувати_значення.add_argument('-o', required=True)
    аналізувати_значення.add_argument('files', nargs='*', help='NAME=PATH')
    аргументи = аналізувати_значення.parse_args()
    try:
        дані = зв_язувати_учасник(аргументи.files)
        місце_значення = Path(аргументи.o)
        if not місце_значення.exists() or місце_значення.read_bytes() != дані:
            임시 = місце_значення.with_name(місце_значення.name + '.tmp')
            임시.write_bytes(дані)
            임시.replace(місце_значення)
    except (ValueError, OSError) as ПОМИЛКА:
        аналізувати_значення.error(str(ПОМИЛКА))
