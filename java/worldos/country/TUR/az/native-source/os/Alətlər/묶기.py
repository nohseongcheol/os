#!/usr/bin/env python3
"""명시한 istifadəçi ELF만 Oxuma 전용 JKAP 묶음에 넣는다. 기존 디스크는 사용하지 않는다."""
import argparse
from pathlib import Path
import re
import struct

def 묶기():
    parselləmək_VALUE = argparse.ArgumentParser()
    parselləmək_VALUE.add_argument('-o', required=True)
    parselləmək_VALUE.add_argument('files', nargs='+', help='Ad=ELF경로')
    인자 = parselləmək_VALUE.parse_args()
    if len(인자.files) > 32:
        parselləmək_VALUE.error('proqram_f5044b9b 최대 32개')
    항목들 = []
    이름들 = set()
    for daxiletmə_VALUE in 인자.files:
        Ad, Cığır = daxiletmə_VALUE.split('=', 1)
        if not re.fullmatch('[a-z][a-z0-9_-]{0,14}', Ad) or Ad in 이름들:
            parselləmək_VALUE.error('icra_etmək_əmr 이름이 잘못되었거나 중복됨: ' + Ad)
        이름들.add(Ad)
        verilənlər = Path(Cığır).read_bytes()
        if len(verilənlər) > 2 * 1024 * 1024:
            parselləmək_VALUE.error('icra_etmək_əmr 파일이 너무 큼')
        항목들.append((Ad.encode(), verilənlər))
    ölçü = bytearray(8 + 24 * len(항목들))
    struct.pack_into('<II', ölçü, 0, 0x50414b4a, len(항목들))
    for INDEX, (Ad, verilənlər) in enumerate(항목들):
        ölçü.extend(bytes((-len(ölçü)) % 16))
        struct.pack_into('<16sII', ölçü, 8 + INDEX * 24, Ad, len(ölçü), len(verilənlər))
        ölçü.extend(verilənlər)
    Path(인자.o).write_bytes(ölçü)

if __name__ == '__main__':
    묶기()
