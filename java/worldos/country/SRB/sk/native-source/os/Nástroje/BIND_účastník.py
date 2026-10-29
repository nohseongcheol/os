#!/usr/bin/env python3
"""명시한 používateľ ELF만 Čítanie 전용 JKAP 묶음에 넣는다. 기존 디스크는 사용하지 않는다."""
import argparse
from pathlib import Path
import re
import struct

def BIND_účastník():
    analyzovať_VALUE = argparse.ArgumentParser()
    analyzovať_VALUE.add_argument('-o', required=True)
    analyzovať_VALUE.add_argument('files', nargs='+', help='Názov=ELF경로')
    parameter_argument = analyzovať_VALUE.parse_args()
    if len(parameter_argument.files) > 32:
        analyzovať_VALUE.error('program_f5044b9b 최대 32개')
    항목들 = []
    이름들 = set()
    for položka_VALUE in parameter_argument.files:
        Názov, Cesta = položka_VALUE.split('=', 1)
        if not re.fullmatch('[a-z][a-z0-9_-]{0,14}', Názov) or Názov in 이름들:
            analyzovať_VALUE.error('Vykonať_príkaz 이름이 잘못되었거나 중복됨: ' + Názov)
        이름들.add(Názov)
        údaje = Path(Cesta).read_bytes()
        if len(údaje) > 2 * 1024 * 1024:
            analyzovať_VALUE.error('Vykonať_príkaz 파일이 너무 큼')
        항목들.append((Názov.encode(), údaje))
    KR = bytearray(8 + 24 * len(항목들))
    struct.pack_into('<II', KR, 0, 0x50414b4a, len(항목들))
    for INDEX, (Názov, údaje) in enumerate(항목들):
        KR.extend(bytes((-len(KR)) % 16))
        struct.pack_into('<16sII', KR, 8 + INDEX * 24, Názov, len(KR), len(údaje))
        KR.extend(údaje)
    Path(parameter_argument.o).write_bytes(KR)

if __name__ == '__main__':
    BIND_účastník()
