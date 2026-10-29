#!/usr/bin/env python3
"""명시한 bruker ELF만 Les 전용 JKAP 묶음에 넣는다. 기존 디스크는 사용하지 않는다."""
import argparse
from pathlib import Path
import re
import struct

def BIND_deltaker():
    dele_opp_VERDI = argparse.ArgumentParser()
    dele_opp_VERDI.add_argument('-o', required=True)
    dele_opp_VERDI.add_argument('files', nargs='+', help='Navn=ELF경로')
    parameter_argument = dele_opp_VERDI.parse_args()
    if len(parameter_argument.files) > 32:
        dele_opp_VERDI.error('app_f5044b9b 최대 32개')
    항목들 = []
    이름들 = set()
    for oppføring_VERDI in parameter_argument.files:
        Navn, Sti = oppføring_VERDI.split('=', 1)
        if not re.fullmatch('[a-z][a-z0-9_-]{0,14}', Navn) or Navn in 이름들:
            dele_opp_VERDI.error('Utfør_kommando 이름이 잘못되었거나 중복됨: ' + Navn)
        이름들.add(Navn)
        data = Path(Sti).read_bytes()
        if len(data) > 2 * 1024 * 1024:
            dele_opp_VERDI.error('Utfør_kommando 파일이 너무 큼')
        항목들.append((Navn.encode(), data))
    KR = bytearray(8 + 24 * len(항목들))
    struct.pack_into('<II', KR, 0, 0x50414b4a, len(항목들))
    for INDEKS, (Navn, data) in enumerate(항목들):
        KR.extend(bytes((-len(KR)) % 16))
        struct.pack_into('<16sII', KR, 8 + INDEKS * 24, Navn, len(KR), len(data))
        KR.extend(data)
    Path(parameter_argument.o).write_bytes(KR)

if __name__ == '__main__':
    BIND_deltaker()
