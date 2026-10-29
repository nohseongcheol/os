#!/usr/bin/env python3
"""명시한 Java источник_дерево/Класс_ЗНАЧЕН 파일을 запуск_машины 시 RAM 파일체계로 가져온다."""
import argparse
from pathlib import Path
import re
import struct


def BIND_участник(항목들):
    파일들 = []
    이름들 = {'Hello.java'}
    명시 = set()
    for ввод_ЗНАЧЕН in 항목들:
        if '=' not in ввод_ЗНАЧЕН:
            raise ValueError('expected NAME=PATH: ' + ввод_ЗНАЧЕН)
        Название, путь = ввод_ЗНАЧЕН.split('=', 1)
        if not re.fullmatch(r'[A-Za-z0-9_-][A-Za-z0-9_.-]{0,62}', Название) or Название in 명시:
            raise ValueError('invalid or duplicate file name: ' + Название)
        명시.add(Название)
        이름들.add(Название)
        данные = Path(путь).read_bytes()
        if len(данные) > 16384:
            raise ValueError('file exceeds 16384 bytes: ' + Название)
        파일들.append((Название.encode('ascii'), данные))
    if len(이름들) > 8:
        raise ValueError('RAM file limit: 8 files including the default Hello.java')
    результат = bytearray(struct.pack('<4sI', b'JKJF', len(파일들)))
    результат.extend(bytes(72 * len(파일들)))
    for 수, (Название, данные) in enumerate(파일들):
        struct.pack_into('<64sII', результат, 8 + 수 * 72, Название, len(результат), len(данные))
        результат.extend(данные)
    return bytes(результат)


if __name__ == '__main__':
    анализировать_ЗНАЧЕН = argparse.ArgumentParser(description=__doc__)
    анализировать_ЗНАЧЕН.add_argument('-o', required=True)
    анализировать_ЗНАЧЕН.add_argument('files', nargs='*', help='NAME=PATH')
    аргументы = анализировать_ЗНАЧЕН.parse_args()
    try:
        данные = BIND_участник(аргументы.files)
        цель_ЗНАЧЕН = Path(аргументы.o)
        if not цель_ЗНАЧЕН.exists() or цель_ЗНАЧЕН.read_bytes() != данные:
            임시 = цель_ЗНАЧЕН.with_name(цель_ЗНАЧЕН.name + '.tmp')
            임시.write_bytes(данные)
            임시.replace(цель_ЗНАЧЕН)
    except (ValueError, OSError) as ошибка:
        анализировать_ЗНАЧЕН.error(str(ошибка))
