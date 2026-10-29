#!/usr/bin/env python3
"""명시한 пространство_пользователя ELF만 Чтение 전용 JKAP 묶음에 넣는다. 기존 디스크는 사용하지 않는다."""
import argparse
from pathlib import Path
import re
import struct

def BIND_участник():
    анализировать_ЗНАЧЕН = argparse.ArgumentParser()
    анализировать_ЗНАЧЕН.add_argument('-o', required=True)
    анализировать_ЗНАЧЕН.add_argument('files', nargs='+', help='Название=ELF경로')
    параметр_аргумент = анализировать_ЗНАЧЕН.parse_args()
    if len(параметр_аргумент.files) > 32:
        анализировать_ЗНАЧЕН.error('программа_f5044b9b 최대 32개')
    항목들 = []
    이름들 = set()
    for ввод_ЗНАЧЕН in параметр_аргумент.files:
        Название, путь = ввод_ЗНАЧЕН.split('=', 1)
        if not re.fullmatch('[a-z][a-z0-9_-]{0,14}', Название) or Название in 이름들:
            анализировать_ЗНАЧЕН.error('실행 이름이 잘못되었거나 중복됨: ' + Название)
        이름들.add(Название)
        данные = Path(путь).read_bytes()
        if len(данные) > 2 * 1024 * 1024:
            анализировать_ЗНАЧЕН.error('실행 파일이 너무 큼')
        항목들.append((Название.encode(), данные))
    результат = bytearray(8 + 24 * len(항목들))
    struct.pack_into('<II', результат, 0, 0x50414b4a, len(항목들))
    for ИНДЕКС, (Название, данные) in enumerate(항목들):
        результат.extend(bytes((-len(результат)) % 16))
        struct.pack_into('<16sII', результат, 8 + ИНДЕКС * 24, Название, len(результат), len(данные))
        результат.extend(данные)
    Path(параметр_аргумент.o).write_bytes(результат)

if __name__ == '__main__':
    BIND_участник()
