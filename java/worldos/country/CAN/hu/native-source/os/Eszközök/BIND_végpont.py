#!/usr/bin/env python3
"""명시한 felhasználó ELF만 Olvasás 전용 JKAP 묶음에 넣는다. 기존 디스크는 사용하지 않는다."""
import argparse
from pathlib import Path
import re
import struct

def BIND_végpont():
    elemez_ÉRTÉK = argparse.ArgumentParser()
    elemez_ÉRTÉK.add_argument('-o', required=True)
    elemez_ÉRTÉK.add_argument('files', nargs='+', help='Név=ELF경로')
    paraméter_argumentum = elemez_ÉRTÉK.parse_args()
    if len(paraméter_argumentum.files) > 32:
        elemez_ÉRTÉK.error('app_f5044b9b 최대 32개')
    항목들 = []
    이름들 = set()
    for bejegyzés_ÉRTÉK in paraméter_argumentum.files:
        Név, ÚTVONAL = bejegyzés_ÉRTÉK.split('=', 1)
        if not re.fullmatch('[a-z][a-z0-9_-]{0,14}', Név) or Név in 이름들:
            elemez_ÉRTÉK.error('végrehajt_parancs 이름이 잘못되었거나 중복됨: ' + Név)
        이름들.add(Név)
        adat = Path(ÚTVONAL).read_bytes()
        if len(adat) > 2 * 1024 * 1024:
            elemez_ÉRTÉK.error('végrehajt_parancs 파일이 너무 큼')
        항목들.append((Név.encode(), adat))
    KR = bytearray(8 + 24 * len(항목들))
    struct.pack_into('<II', KR, 0, 0x50414b4a, len(항목들))
    for INDEX, (Név, adat) in enumerate(항목들):
        KR.extend(bytes((-len(KR)) % 16))
        struct.pack_into('<16sII', KR, 8 + INDEX * 24, Név, len(KR), len(adat))
        KR.extend(adat)
    Path(paraméter_argumentum.o).write_bytes(KR)

if __name__ == '__main__':
    BIND_végpont()
