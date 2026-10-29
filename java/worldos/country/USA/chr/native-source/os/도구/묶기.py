#!/usr/bin/env python3
"""명시한 ᎬᏗᏍᎩ ELF만 읽기 전용 JKAP 묶음에 넣는다. 기존 디스크는 사용하지 않는다."""
import argparse
from pathlib import Path
import re
import struct

def 묶기():
    해석 = argparse.ArgumentParser()
    해석.add_argument('-o', required=True)
    해석.add_argument('files', nargs='+', help='ᏚᏙᎥᎢ=ELF경로')
    인자 = 해석.parse_args()
    if len(인자.files) > 32:
        해석.error('ᎬᏙᏗ_f5044b9b 최대 32개')
    항목들 = []
    이름들 = set()
    for Ꭵ_ᎧᏁᏉᎢᏍᏙᏗ_ᏧᎬᏩᎶᏗᏯ in 인자.files:
        ᏚᏙᎥᎢ, ᎠᏍᏓᏩᏛᏍᏗ = Ꭵ_ᎧᏁᏉᎢᏍᏙᏗ_ᏧᎬᏩᎶᏗᏯ.split('=', 1)
        if not re.fullmatch('[a-z][a-z0-9_-]{0,14}', ᏚᏙᎥᎢ) or ᏚᏙᎥᎢ in 이름들:
            해석.error('ᎠᎴᏅᏗᏱ_ᎤᏁᏤᎸᎩ 이름이 잘못되었거나 중복됨: ' + ᏚᏙᎥᎢ)
        이름들.add(ᏚᏙᎥᎢ)
        ᎦᏟᏌᏅᎯ = Path(ᎠᏍᏓᏩᏛᏍᏗ).read_bytes()
        if len(ᎦᏟᏌᏅᎯ) > 2 * 1024 * 1024:
            해석.error('ᎠᎴᏅᏗᏱ_ᎤᏁᏤᎸᎩ 파일이 너무 큼')
        항목들.append((ᏚᏙᎥᎢ.encode(), ᎦᏟᏌᏅᎯ))
    결과 = bytearray(8 + 24 * len(항목들))
    struct.pack_into('<II', 결과, 0, 0x50414b4a, len(항목들))
    for ᏂᎬᎿᏅ_ᎠᏓᏎᎮᎯ, (ᏚᏙᎥᎢ, ᎦᏟᏌᏅᎯ) in enumerate(항목들):
        결과.extend(bytes((-len(결과)) % 16))
        struct.pack_into('<16sII', 결과, 8 + ᏂᎬᎿᏅ_ᎠᏓᏎᎮᎯ * 24, ᏚᏙᎥᎢ, len(결과), len(ᎦᏟᏌᏅᎯ))
        결과.extend(ᎦᏟᏌᏅᎯ)
    Path(인자.o).write_bytes(결과)

if __name__ == '__main__':
    묶기()
