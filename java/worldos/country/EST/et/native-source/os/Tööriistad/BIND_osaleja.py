#!/usr/bin/env python3
"""명시한 kasutaja ELF만 Lugemine 전용 JKAP 묶음에 넣는다. 기존 디스크는 사용하지 않는다."""
import argparse
from pathlib import Path
import re
import struct

def BIND_osaleja():
    sõeluma_VALUE = argparse.ArgumentParser()
    sõeluma_VALUE.add_argument('-o', required=True)
    sõeluma_VALUE.add_argument('files', nargs='+', help='Nimi_2=ELF경로')
    parameeter_argument = sõeluma_VALUE.parse_args()
    if len(parameeter_argument.files) > 32:
        sõeluma_VALUE.error('programm_f5044b9b 최대 32개')
    항목들 = []
    이름들 = set()
    for kirje_VALUE in parameeter_argument.files:
        Nimi_2, RADA = kirje_VALUE.split('=', 1)
        if not re.fullmatch('[a-z][a-z0-9_-]{0,14}', Nimi_2) or Nimi_2 in 이름들:
            sõeluma_VALUE.error('Täida_käsk 이름이 잘못되었거나 중복됨: ' + Nimi_2)
        이름들.add(Nimi_2)
        andmed = Path(RADA).read_bytes()
        if len(andmed) > 2 * 1024 * 1024:
            sõeluma_VALUE.error('Täida_käsk 파일이 너무 큼')
        항목들.append((Nimi_2.encode(), andmed))
    TULEMUS = bytearray(8 + 24 * len(항목들))
    struct.pack_into('<II', TULEMUS, 0, 0x50414b4a, len(항목들))
    for INDEX, (Nimi_2, andmed) in enumerate(항목들):
        TULEMUS.extend(bytes((-len(TULEMUS)) % 16))
        struct.pack_into('<16sII', TULEMUS, 8 + INDEX * 24, Nimi_2, len(TULEMUS), len(andmed))
        TULEMUS.extend(andmed)
    Path(parameeter_argument.o).write_bytes(TULEMUS)

if __name__ == '__main__':
    BIND_osaleja()
