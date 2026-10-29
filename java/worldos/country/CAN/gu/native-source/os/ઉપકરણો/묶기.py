#!/usr/bin/env python3
"""명시한 ઉપયોગકર્તા ELF만 વાંચો 전용 JKAP 묶음에 넣는다. 기존 디스크는 사용하지 않는다."""
import argparse
from pathlib import Path
import re
import struct

def 묶기():
    પાર્સ_કરો_મૂલ્ય = argparse.ArgumentParser()
    પાર્સ_કરો_મૂલ્ય.add_argument('-o', required=True)
    પાર્સ_કરો_મૂલ્ય.add_argument('files', nargs='+', help='નામ=ELF경로')
    પેરામીટર_દલીલ = પાર્સ_કરો_મૂલ્ય.parse_args()
    if len(પેરામીટર_દલીલ.files) > 32:
        પાર્સ_કરો_મૂલ્ય.error('એપ્લિકેશન_f5044b9b 최대 32개')
    항목들 = []
    이름들 = set()
    for પ્રવેશ_મૂલ્ય in પેરામીટર_દલીલ.files:
        નામ, પથ = પ્રવેશ_મૂલ્ય.split('=', 1)
        if not re.fullmatch('[a-z][a-z0-9_-]{0,14}', નામ) or નામ in 이름들:
            પાર્સ_કરો_મૂલ્ય.error('અમલ_કરો_આદેશ 이름이 잘못되었거나 중복됨: ' + નામ)
        이름들.add(નામ)
        ડેટા = Path(પથ).read_bytes()
        if len(ડેટા) > 2 * 1024 * 1024:
            પાર્સ_કરો_મૂલ્ય.error('અમલ_કરો_આદેશ 파일이 너무 큼')
        항목들.append((નામ.encode(), ડેટા))
    પરિમાણ = bytearray(8 + 24 * len(항목들))
    struct.pack_into('<II', પરિમાણ, 0, 0x50414b4a, len(항목들))
    for અનુક્રમણિકા, (નામ, ડેટા) in enumerate(항목들):
        પરિમાણ.extend(bytes((-len(પરિમાણ)) % 16))
        struct.pack_into('<16sII', પરિમાણ, 8 + અનુક્રમણિકા * 24, નામ, len(પરિમાણ), len(ડેટા))
        પરિમાણ.extend(ડેટા)
    Path(પેરામીટર_દલીલ.o).write_bytes(પરિમાણ)

if __name__ == '__main__':
    묶기()
