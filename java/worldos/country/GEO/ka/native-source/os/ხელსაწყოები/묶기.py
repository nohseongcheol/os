#!/usr/bin/env python3
"""명시한 მომხმარებელი ELF만 კითხვა 전용 JKAP 묶음에 넣는다. 기존 디스크는 사용하지 않는다."""
import argparse
from pathlib import Path
import re
import struct

def 묶기():
    ანალიზი_მნიშვნელობა = argparse.ArgumentParser()
    ანალიზი_მნიშვნელობა.add_argument('-o', required=True)
    ანალიზი_მნიშვნელობა.add_argument('files', nargs='+', help='სახელი=ELF경로')
    인자 = ანალიზი_მნიშვნელობა.parse_args()
    if len(인자.files) > 32:
        ანალიზი_მნიშვნელობა.error('აპი_f5044b9b 최대 32개')
    항목들 = []
    이름들 = set()
    for შენატანი_მნიშვნელობა in 인자.files:
        სახელი, გეზი = შენატანი_მნიშვნელობა.split('=', 1)
        if not re.fullmatch('[a-z][a-z0-9_-]{0,14}', სახელი) or სახელი in 이름들:
            ანალიზი_მნიშვნელობა.error('შესრულება_ბრძანება 이름이 잘못되었거나 중복됨: ' + სახელი)
        이름들.add(სახელი)
        მონაცემები = Path(გეზი).read_bytes()
        if len(მონაცემები) > 2 * 1024 * 1024:
            ანალიზი_მნიშვნელობა.error('შესრულება_ბრძანება 파일이 너무 큼')
        항목들.append((სახელი.encode(), მონაცემები))
    გაზომვა = bytearray(8 + 24 * len(항목들))
    struct.pack_into('<II', გაზომვა, 0, 0x50414b4a, len(항목들))
    for ინდექსი, (სახელი, მონაცემები) in enumerate(항목들):
        გაზომვა.extend(bytes((-len(გაზომვა)) % 16))
        struct.pack_into('<16sII', გაზომვა, 8 + ინდექსი * 24, სახელი, len(გაზომვა), len(მონაცემები))
        გაზომვა.extend(მონაცემები)
    Path(인자.o).write_bytes(გაზომვა)

if __name__ == '__main__':
    묶기()
