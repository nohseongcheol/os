#!/usr/bin/env python3
"""명시한 بەکارهێنەر ELF만 읽기 전용 JKAP 묶음에 넣는다. 기존 디스크는 사용하지 않는다."""
import argparse
from pathlib import Path
import re
import struct

def 묶기():
    해석 = argparse.ArgumentParser()
    해석.add_argument('-o', required=True)
    해석.add_argument('files', nargs='+', help='ناو=ELF경로')
    인자 = 해석.parse_args()
    if len(인자.files) > 32:
        해석.error('بەرنامە_f5044b9b 최대 32개')
    항목들 = []
    이름들 = set()
    for تێنووسین_نرخ in 인자.files:
        ناو, گوزەر = تێنووسین_نرخ.split('=', 1)
        if not re.fullmatch('[a-z][a-z0-9_-]{0,14}', ناو) or ناو in 이름들:
            해석.error('جێبەجێکردن_فەرمان 이름이 잘못되었거나 중복됨: ' + ناو)
        이름들.add(ناو)
        دەیتا = Path(گوزەر).read_bytes()
        if len(دەیتا) > 2 * 1024 * 1024:
            해석.error('جێبەجێکردن_فەرمان 파일이 너무 큼')
        항목들.append((ناو.encode(), دەیتا))
    결과 = bytearray(8 + 24 * len(항목들))
    struct.pack_into('<II', 결과, 0, 0x50414b4a, len(항목들))
    for پێرست, (ناو, دەیتا) in enumerate(항목들):
        결과.extend(bytes((-len(결과)) % 16))
        struct.pack_into('<16sII', 결과, 8 + پێرست * 24, ناو, len(결과), len(دەیتا))
        결과.extend(دەیتا)
    Path(인자.o).write_bytes(결과)

if __name__ == '__main__':
    묶기()
