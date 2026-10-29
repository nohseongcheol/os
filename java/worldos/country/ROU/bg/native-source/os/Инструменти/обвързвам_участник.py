#!/usr/bin/env python3
"""명시한 потребител ELF만 Четене 전용 JKAP 묶음에 넣는다. 기존 디스크는 사용하지 않는다."""
import argparse
from pathlib import Path
import re
import struct

def обвързвам_участник():
    анализирам_стойност = argparse.ArgumentParser()
    анализирам_стойност.add_argument('-o', required=True)
    анализирам_стойност.add_argument('files', nargs='+', help='Име=ELF경로')
    параметър_аргумент = анализирам_стойност.parse_args()
    if len(параметър_аргумент.files) > 32:
        анализирам_стойност.error('програма_f5044b9b 최대 32개')
    항목들 = []
    이름들 = set()
    for запис_стойност in параметър_аргумент.files:
        Име, ПЪТ = запис_стойност.split('=', 1)
        if not re.fullmatch('[a-z][a-z0-9_-]{0,14}', Име) or Име in 이름들:
            анализирам_стойност.error('изпълнявам_команда 이름이 잘못되었거나 중복됨: ' + Име)
        이름들.add(Име)
        данни = Path(ПЪТ).read_bytes()
        if len(данни) > 2 * 1024 * 1024:
            анализирам_стойност.error('изпълнявам_команда 파일이 너무 큼')
        항목들.append((Име.encode(), данни))
    РЕЗУЛТАТ = bytearray(8 + 24 * len(항목들))
    struct.pack_into('<II', РЕЗУЛТАТ, 0, 0x50414b4a, len(항목들))
    for индекс, (Име, данни) in enumerate(항목들):
        РЕЗУЛТАТ.extend(bytes((-len(РЕЗУЛТАТ)) % 16))
        struct.pack_into('<16sII', РЕЗУЛТАТ, 8 + индекс * 24, Име, len(РЕЗУЛТАТ), len(данни))
        РЕЗУЛТАТ.extend(данни)
    Path(параметър_аргумент.o).write_bytes(РЕЗУЛТАТ)

if __name__ == '__main__':
    обвързвам_участник()
