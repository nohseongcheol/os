#!/usr/bin/env python3
"""명시한 корбар ELF만 Хондан 전용 JKAP 묶음에 넣는다. 기존 디스크는 사용하지 않는다."""
import argparse
from pathlib import Path
import re
import struct

def 묶기():
    해석 = argparse.ArgumentParser()
    해석.add_argument('-o', required=True)
    해석.add_argument('files', nargs='+', help='Ном=ELF경로')
    인자 = 해석.parse_args()
    if len(인자.files) > 32:
        해석.error('барнома_f5044b9b 최대 32개')
    항목들 = []
    이름들 = set()
    for ворида_қимат in 인자.files:
        Ном, масир = ворида_қимат.split('=', 1)
        if not re.fullmatch('[a-z][a-z0-9_-]{0,14}', Ном) or Ном in 이름들:
            해석.error('иҷро_кардан_фармон 이름이 잘못되었거나 중복됨: ' + Ном)
        이름들.add(Ном)
        иттилоот = Path(масир).read_bytes()
        if len(иттилоот) > 2 * 1024 * 1024:
            해석.error('иҷро_кардан_фармон 파일이 너무 큼')
        항목들.append((Ном.encode(), иттилоот))
    결과 = bytearray(8 + 24 * len(항목들))
    struct.pack_into('<II', 결과, 0, 0x50414b4a, len(항목들))
    for индекс, (Ном, иттилоот) in enumerate(항목들):
        결과.extend(bytes((-len(결과)) % 16))
        struct.pack_into('<16sII', 결과, 8 + индекс * 24, Ном, len(결과), len(иттилоот))
        결과.extend(иттилоот)
    Path(인자.o).write_bytes(결과)

if __name__ == '__main__':
    묶기()
