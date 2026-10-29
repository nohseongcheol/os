#!/usr/bin/env python3
"""명시한 простір_користувача ELF만 Читання 전용 JKAP 묶음에 넣는다. 기존 디스크는 사용하지 않는다."""
import argparse
from pathlib import Path
import re
import struct

def зв_язувати_учасник():
    аналізувати_значення = argparse.ArgumentParser()
    аналізувати_значення.add_argument('-o', required=True)
    аналізувати_значення.add_argument('files', nargs='+', help='Назва=ELF경로')
    параметр_аргумент = аналізувати_значення.parse_args()
    if len(параметр_аргумент.files) > 32:
        аналізувати_значення.error('програма_f5044b9b 최대 32개')
    항목들 = []
    이름들 = set()
    for запис_значення_962f286b in параметр_аргумент.files:
        Назва, шлях = запис_значення_962f286b.split('=', 1)
        if not re.fullmatch('[a-z][a-z0-9_-]{0,14}', Назва) or Назва in 이름들:
            аналізувати_значення.error('Виконати_команда 이름이 잘못되었거나 중복됨: ' + Назва)
        이름들.add(Назва)
        дані = Path(шлях).read_bytes()
        if len(дані) > 2 * 1024 * 1024:
            аналізувати_значення.error('Виконати_команда 파일이 너무 큼')
        항목들.append((Назва.encode(), дані))
    результат = bytearray(8 + 24 * len(항목들))
    struct.pack_into('<II', результат, 0, 0x50414b4a, len(항목들))
    for індекс, (Назва, дані) in enumerate(항목들):
        результат.extend(bytes((-len(результат)) % 16))
        struct.pack_into('<16sII', результат, 8 + індекс * 24, Назва, len(результат), len(дані))
        результат.extend(дані)
    Path(параметр_аргумент.o).write_bytes(результат)

if __name__ == '__main__':
    зв_язувати_учасник()
