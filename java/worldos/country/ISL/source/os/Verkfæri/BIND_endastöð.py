#!/usr/bin/env python3
"""명시한 notandi ELF만 Lestur 전용 JKAP 묶음에 넣는다. 기존 디스크는 사용하지 않는다."""
import argparse
from pathlib import Path
import re
import struct

def BIND_endastöð():
    þátta_VALUE = argparse.ArgumentParser()
    þátta_VALUE.add_argument('-o', required=True)
    þátta_VALUE.add_argument('files', nargs='+', help='Heiti=ELF경로')
    færibreyta_frumbreyta = þátta_VALUE.parse_args()
    if len(færibreyta_frumbreyta.files) > 32:
        þátta_VALUE.error('forrit_f5044b9b 최대 32개')
    항목들 = []
    이름들 = set()
    for færsla_VALUE in færibreyta_frumbreyta.files:
        Heiti, SLÓÐ = færsla_VALUE.split('=', 1)
        if not re.fullmatch('[a-z][a-z0-9_-]{0,14}', Heiti) or Heiti in 이름들:
            þátta_VALUE.error('keyra_skipun 이름이 잘못되었거나 중복됨: ' + Heiti)
        이름들.add(Heiti)
        gögn = Path(SLÓÐ).read_bytes()
        if len(gögn) > 2 * 1024 * 1024:
            þátta_VALUE.error('keyra_skipun 파일이 너무 큼')
        항목들.append((Heiti.encode(), gögn))
    NIÐURSTAÐA = bytearray(8 + 24 * len(항목들))
    struct.pack_into('<II', NIÐURSTAÐA, 0, 0x50414b4a, len(항목들))
    for INDEX, (Heiti, gögn) in enumerate(항목들):
        NIÐURSTAÐA.extend(bytes((-len(NIÐURSTAÐA)) % 16))
        struct.pack_into('<16sII', NIÐURSTAÐA, 8 + INDEX * 24, Heiti, len(NIÐURSTAÐA), len(gögn))
        NIÐURSTAÐA.extend(gögn)
    Path(færibreyta_frumbreyta.o).write_bytes(NIÐURSTAÐA)

if __name__ == '__main__':
    BIND_endastöð()
