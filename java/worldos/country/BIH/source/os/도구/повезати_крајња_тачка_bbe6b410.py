#!/usr/bin/env python3
"""명시한 корисник ELF만 읽기 전용 JKAP 묶음에 넣는다. 기존 디스크는 사용하지 않는다."""
import argparse
from pathlib import Path
import re
import struct

def повезати_крајња_тачка_bbe6b410():
    рашчлањивати_вриједност = argparse.ArgumentParser()
    рашчлањивати_вриједност.add_argument('-o', required=True)
    рашчлањивати_вриједност.add_argument('files', nargs='+', help='назив=ELF경로')
    인자 = рашчлањивати_вриједност.parse_args()
    if len(인자.files) > 32:
        рашчлањивати_вриједност.error('програм_f5044b9b 최대 32개')
    항목들 = []
    이름들 = set()
    for унос_вриједност in 인자.files:
        назив, пут = унос_вриједност.split('=', 1)
        if not re.fullmatch('[a-z][a-z0-9_-]{0,14}', назив) or назив in 이름들:
            рашчлањивати_вриједност.error('실행 이름이 잘못되었거나 중복됨: ' + назив)
        이름들.add(назив)
        подаци = Path(пут).read_bytes()
        if len(подаци) > 2 * 1024 * 1024:
            рашчлањивати_вриједност.error('실행 파일이 너무 큼')
        항목들.append((назив.encode(), подаци))
    결과 = bytearray(8 + 24 * len(항목들))
    struct.pack_into('<II', 결과, 0, 0x50414b4a, len(항목들))
    for индекс, (назив, подаци) in enumerate(항목들):
        결과.extend(bytes((-len(결과)) % 16))
        struct.pack_into('<16sII', 결과, 8 + индекс * 24, назив, len(결과), len(подаци))
        결과.extend(подаци)
    Path(인자.o).write_bytes(결과)

if __name__ == '__main__':
    повезати_крајња_тачка_bbe6b410()
