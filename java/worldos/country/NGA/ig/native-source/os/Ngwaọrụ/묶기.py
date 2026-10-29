#!/usr/bin/env python3
"""명시한 òjìàrụ ELF만 Wepụta_ọzi 전용 JKAP 묶음에 넣는다. 기존 디스크는 사용하지 않는다."""
import argparse
from pathlib import Path
import re
import struct

def 묶기():
    kerìsịa_valuu = argparse.ArgumentParser()
    kerìsịa_valuu.add_argument('-o', required=True)
    kerìsịa_valuu.add_argument('files', nargs='+', help='Aha=ELF경로')
    인자 = kerìsịa_valuu.parse_args()
    if len(인자.files) > 32:
        kerìsịa_valuu.error('app_f5044b9b 최대 32개')
    항목들 = []
    이름들 = set()
    for ndebà_valuu in 인자.files:
        Aha, ụzọ_ozi = ndebà_valuu.split('=', 1)
        if not re.fullmatch('[a-z][a-z0-9_-]{0,14}', Aha) or Aha in 이름들:
            kerìsịa_valuu.error('mee_nnyemiwu 이름이 잘못되었거나 중복됨: ' + Aha)
        이름들.add(Aha)
        datà = Path(ụzọ_ozi).read_bytes()
        if len(datà) > 2 * 1024 * 1024:
            kerìsịa_valuu.error('mee_nnyemiwu 파일이 너무 큼')
        항목들.append((Aha.encode(), datà))
    결과 = bytearray(8 + 24 * len(항목들))
    struct.pack_into('<II', 결과, 0, 0x50414b4a, len(항목들))
    for indèks, (Aha, datà) in enumerate(항목들):
        결과.extend(bytes((-len(결과)) % 16))
        struct.pack_into('<16sII', 결과, 8 + indèks * 24, Aha, len(결과), len(datà))
        결과.extend(datà)
    Path(인자.o).write_bytes(결과)

if __name__ == '__main__':
    묶기()
