#!/usr/bin/env python3
"""명시한 përdorues ELF만 Leximi 전용 JKAP 묶음에 넣는다. 기존 디스크는 사용하지 않는다."""
import argparse
from pathlib import Path
import re
import struct

def 묶기():
    analizoj_VALUE = argparse.ArgumentParser()
    analizoj_VALUE.add_argument('-o', required=True)
    analizoj_VALUE.add_argument('files', nargs='+', help='Emër=ELF경로')
    parametër_argument = analizoj_VALUE.parse_args()
    if len(parametër_argument.files) > 32:
        analizoj_VALUE.error('program_f5044b9b 최대 32개')
    항목들 = []
    이름들 = set()
    for futje_VALUE in parametër_argument.files:
        Emër, POZICIONI = futje_VALUE.split('=', 1)
        if not re.fullmatch('[a-z][a-z0-9_-]{0,14}', Emër) or Emër in 이름들:
            analizoj_VALUE.error('zbatoj_komandë 이름이 잘못되었거나 중복됨: ' + Emër)
        이름들.add(Emër)
        të_dhëna = Path(POZICIONI).read_bytes()
        if len(të_dhëna) > 2 * 1024 * 1024:
            analizoj_VALUE.error('zbatoj_komandë 파일이 너무 큼')
        항목들.append((Emër.encode(), të_dhëna))
    llogaritje = bytearray(8 + 24 * len(항목들))
    struct.pack_into('<II', llogaritje, 0, 0x50414b4a, len(항목들))
    for INDEX, (Emër, të_dhëna) in enumerate(항목들):
        llogaritje.extend(bytes((-len(llogaritje)) % 16))
        struct.pack_into('<16sII', llogaritje, 8 + INDEX * 24, Emër, len(llogaritje), len(të_dhëna))
        llogaritje.extend(të_dhëna)
    Path(parametër_argument.o).write_bytes(llogaritje)

if __name__ == '__main__':
    묶기()
