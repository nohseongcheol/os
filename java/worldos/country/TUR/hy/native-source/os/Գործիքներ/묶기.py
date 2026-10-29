#!/usr/bin/env python3
"""명시한 օգտվող ELF만 Ընթերցում 전용 JKAP 묶음에 넣는다. 기존 디스크는 사용하지 않는다."""
import argparse
from pathlib import Path
import re
import struct

def 묶기():
    վերլուծել_արժեք = argparse.ArgumentParser()
    վերլուծել_արժեք.add_argument('-o', required=True)
    վերլուծել_արժեք.add_argument('files', nargs='+', help='Անուն=ELF경로')
    인자 = վերլուծել_արժեք.parse_args()
    if len(인자.files) > 32:
        վերլուծել_արժեք.error('ծրագիր_f5044b9b 최대 32개')
    항목들 = []
    이름들 = set()
    for մուտքագրում_արժեք in 인자.files:
        Անուն, Ճանապարհ = մուտքագրում_արժեք.split('=', 1)
        if not re.fullmatch('[a-z][a-z0-9_-]{0,14}', Անուն) or Անուն in 이름들:
            վերլուծել_արժեք.error('կատարել_հրաման 이름이 잘못되었거나 중복됨: ' + Անուն)
        이름들.add(Անուն)
        տվյալ = Path(Ճանապարհ).read_bytes()
        if len(տվյալ) > 2 * 1024 * 1024:
            վերլուծել_արժեք.error('կատարել_հրաման 파일이 너무 큼')
        항목들.append((Անուն.encode(), տվյալ))
    չափ = bytearray(8 + 24 * len(항목들))
    struct.pack_into('<II', չափ, 0, 0x50414b4a, len(항목들))
    for դասիչ, (Անուն, տվյալ) in enumerate(항목들):
        չափ.extend(bytes((-len(չափ)) % 16))
        struct.pack_into('<16sII', չափ, 8 + դասիչ * 24, Անուն, len(չափ), len(տվյալ))
        չափ.extend(տվյալ)
    Path(인자.o).write_bytes(չափ)

if __name__ == '__main__':
    묶기()
