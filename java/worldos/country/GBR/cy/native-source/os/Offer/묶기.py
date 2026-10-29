#!/usr/bin/env python3
"""명시한 defnyddiwr ELF만 Darllen 전용 JKAP 묶음에 넣는다. 기존 디스크는 사용하지 않는다."""
import argparse
from pathlib import Path
import re
import struct

def 묶기():
    dosrannu_VALUE = argparse.ArgumentParser()
    dosrannu_VALUE.add_argument('-o', required=True)
    dosrannu_VALUE.add_argument('files', nargs='+', help='Enw=ELF경로')
    paramedr_arg = dosrannu_VALUE.parse_args()
    if len(paramedr_arg.files) > 32:
        dosrannu_VALUE.error('Rhaglen_f5044b9b 최대 32개')
    항목들 = []
    이름들 = set()
    for cofnod_VALUE in paramedr_arg.files:
        Enw, LLWYBR = cofnod_VALUE.split('=', 1)
        if not re.fullmatch('[a-z][a-z0-9_-]{0,14}', Enw) or Enw in 이름들:
            dosrannu_VALUE.error('Gweithredu_gorchymyn 이름이 잘못되었거나 중복됨: ' + Enw)
        이름들.add(Enw)
        data = Path(LLWYBR).read_bytes()
        if len(data) > 2 * 1024 * 1024:
            dosrannu_VALUE.error('Gweithredu_gorchymyn 파일이 너무 큼')
        항목들.append((Enw.encode(), data))
    mesur = bytearray(8 + 24 * len(항목들))
    struct.pack_into('<II', mesur, 0, 0x50414b4a, len(항목들))
    for INDEX, (Enw, data) in enumerate(항목들):
        mesur.extend(bytes((-len(mesur)) % 16))
        struct.pack_into('<16sII', mesur, 8 + INDEX * 24, Enw, len(mesur), len(data))
        mesur.extend(data)
    Path(paramedr_arg.o).write_bytes(mesur)

if __name__ == '__main__':
    묶기()
