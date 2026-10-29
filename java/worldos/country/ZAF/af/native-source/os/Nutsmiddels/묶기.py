#!/usr/bin/env python3
"""명시한 gebruiker ELF만 Lees 전용 JKAP 묶음에 넣는다. 기존 디스크는 사용하지 않는다."""
import argparse
from pathlib import Path
import re
import struct

def 묶기():
    ontleed_VALUE = argparse.ArgumentParser()
    ontleed_VALUE.add_argument('-o', required=True)
    ontleed_VALUE.add_argument('files', nargs='+', help='Naam=ELF경로')
    인자 = ontleed_VALUE.parse_args()
    if len(인자.files) > 32:
        ontleed_VALUE.error('program_f5044b9b 최대 32개')
    항목들 = []
    이름들 = set()
    for inskrywing_VALUE in 인자.files:
        Naam, Pad = inskrywing_VALUE.split('=', 1)
        if not re.fullmatch('[a-z][a-z0-9_-]{0,14}', Naam) or Naam in 이름들:
            ontleed_VALUE.error('uitvoer_bevel 이름이 잘못되었거나 중복됨: ' + Naam)
        이름들.add(Naam)
        data = Path(Pad).read_bytes()
        if len(data) > 2 * 1024 * 1024:
            ontleed_VALUE.error('uitvoer_bevel 파일이 너무 큼')
        항목들.append((Naam.encode(), data))
    maatreël = bytearray(8 + 24 * len(항목들))
    struct.pack_into('<II', maatreël, 0, 0x50414b4a, len(항목들))
    for INDEX, (Naam, data) in enumerate(항목들):
        maatreël.extend(bytes((-len(maatreël)) % 16))
        struct.pack_into('<16sII', maatreël, 8 + INDEX * 24, Naam, len(maatreël), len(data))
        maatreël.extend(data)
    Path(인자.o).write_bytes(maatreël)

if __name__ == '__main__':
    묶기()
