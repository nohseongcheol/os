#!/usr/bin/env python3
"""명시한 lietotājs ELF만 Lasīt 전용 JKAP 묶음에 넣는다. 기존 디스크는 사용하지 않는다."""
import argparse
from pathlib import Path
import re
import struct

def BIND_dalībnieks():
    parsēt_VALUE = argparse.ArgumentParser()
    parsēt_VALUE.add_argument('-o', required=True)
    parsēt_VALUE.add_argument('files', nargs='+', help='Nosaukums=ELF경로')
    parametrs_arg = parsēt_VALUE.parse_args()
    if len(parametrs_arg.files) > 32:
        parsēt_VALUE.error('programma_f5044b9b 최대 32개')
    항목들 = []
    이름들 = set()
    for ievade_VALUE in parametrs_arg.files:
        Nosaukums, CEĻŠ = ievade_VALUE.split('=', 1)
        if not re.fullmatch('[a-z][a-z0-9_-]{0,14}', Nosaukums) or Nosaukums in 이름들:
            parsēt_VALUE.error('Izpildīt_komanda 이름이 잘못되었거나 중복됨: ' + Nosaukums)
        이름들.add(Nosaukums)
        dati = Path(CEĻŠ).read_bytes()
        if len(dati) > 2 * 1024 * 1024:
            parsēt_VALUE.error('Izpildīt_komanda 파일이 너무 큼')
        항목들.append((Nosaukums.encode(), dati))
    mērs = bytearray(8 + 24 * len(항목들))
    struct.pack_into('<II', mērs, 0, 0x50414b4a, len(항목들))
    for INDEX, (Nosaukums, dati) in enumerate(항목들):
        mērs.extend(bytes((-len(mērs)) % 16))
        struct.pack_into('<16sII', mērs, 8 + INDEX * 24, Nosaukums, len(mērs), len(dati))
        mērs.extend(dati)
    Path(parametrs_arg.o).write_bytes(mērs)

if __name__ == '__main__':
    BIND_dalībnieks()
