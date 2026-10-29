#!/usr/bin/env python3
"""명시한 umsebenzisi ELF만 Funda 전용 JKAP 묶음에 넣는다. 기존 디스크는 사용하지 않는다."""
import argparse
from pathlib import Path
import re
import struct

def 묶기():
    zawula_inani = argparse.ArgumentParser()
    zawula_inani.add_argument('-o', required=True)
    zawula_inani.add_argument('files', nargs='+', help='Igama=ELF경로')
    인자 = zawula_inani.parse_args()
    if len(인자.files) > 32:
        zawula_inani.error('i_app_f5044b9b 최대 32개')
    항목들 = []
    이름들 = set()
    for okufakwayo_inani in 인자.files:
        Igama, Indlela_2 = okufakwayo_inani.split('=', 1)
        if not re.fullmatch('[a-z][a-z0-9_-]{0,14}', Igama) or Igama in 이름들:
            zawula_inani.error('yenza_umyalo 이름이 잘못되었거나 중복됨: ' + Igama)
        이름들.add(Igama)
        imininingwane = Path(Indlela_2).read_bytes()
        if len(imininingwane) > 2 * 1024 * 1024:
            zawula_inani.error('yenza_umyalo 파일이 너무 큼')
        항목들.append((Igama.encode(), imininingwane))
    결과 = bytearray(8 + 24 * len(항목들))
    struct.pack_into('<II', 결과, 0, 0x50414b4a, len(항목들))
    for thola_inkomba, (Igama, imininingwane) in enumerate(항목들):
        결과.extend(bytes((-len(결과)) % 16))
        struct.pack_into('<16sII', 결과, 8 + thola_inkomba * 24, Igama, len(결과), len(imininingwane))
        결과.extend(imininingwane)
    Path(인자.o).write_bytes(결과)

if __name__ == '__main__':
    묶기()
