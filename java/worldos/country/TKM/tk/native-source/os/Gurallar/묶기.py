#!/usr/bin/env python3
"""명시한 ulanyjy ELF만 Oka 전용 JKAP 묶음에 넣는다. 기존 디스크는 사용하지 않는다."""
import argparse
from pathlib import Path
import re
import struct

def 묶기():
    seljer_baha = argparse.ArgumentParser()
    seljer_baha.add_argument('-o', required=True)
    seljer_baha.add_argument('files', nargs='+', help='Ad=ELF경로')
    인자 = seljer_baha.parse_args()
    if len(인자.files) > 32:
        seljer_baha.error('programma_f5044b9b 최대 32개')
    항목들 = []
    이름들 = set()
    for girizmeklik_baha in 인자.files:
        Ad, Ýol = girizmeklik_baha.split('=', 1)
        if not re.fullmatch('[a-z][a-z0-9_-]{0,14}', Ad) or Ad in 이름들:
            seljer_baha.error('ýerine_ýetir_buýruk 이름이 잘못되었거나 중복됨: ' + Ad)
        이름들.add(Ad)
        maglumat = Path(Ýol).read_bytes()
        if len(maglumat) > 2 * 1024 * 1024:
            seljer_baha.error('ýerine_ýetir_buýruk 파일이 너무 큼')
        항목들.append((Ad.encode(), maglumat))
    결과 = bytearray(8 + 24 * len(항목들))
    struct.pack_into('<II', 결과, 0, 0x50414b4a, len(항목들))
    for indeks, (Ad, maglumat) in enumerate(항목들):
        결과.extend(bytes((-len(결과)) % 16))
        struct.pack_into('<16sII', 결과, 8 + indeks * 24, Ad, len(결과), len(maglumat))
        결과.extend(maglumat)
    Path(인자.o).write_bytes(결과)

if __name__ == '__main__':
    묶기()
