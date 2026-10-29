#!/usr/bin/env python3
"""명시한 kaiwhakamahi ELF만 Pānuitia 전용 JKAP 묶음에 넣는다. 기존 디스크는 사용하지 않는다."""
import argparse
from pathlib import Path
import re
import struct

def 묶기():
    poroporo_uara = argparse.ArgumentParser()
    poroporo_uara.add_argument('-o', required=True)
    poroporo_uara.add_argument('files', nargs='+', help='Ingoa=ELF경로')
    인자 = poroporo_uara.parse_args()
    if len(인자.files) > 32:
        poroporo_uara.error('kaupapa_f5044b9b 최대 32개')
    항목들 = []
    이름들 = set()
    for tāurunga_uara in 인자.files:
        Ingoa, ara = tāurunga_uara.split('=', 1)
        if not re.fullmatch('[a-z][a-z0-9_-]{0,14}', Ingoa) or Ingoa in 이름들:
            poroporo_uara.error('kawe_tono 이름이 잘못되었거나 중복됨: ' + Ingoa)
        이름들.add(Ingoa)
        raraunga = Path(ara).read_bytes()
        if len(raraunga) > 2 * 1024 * 1024:
            poroporo_uara.error('kawe_tono 파일이 너무 큼')
        항목들.append((Ingoa.encode(), raraunga))
    mēhua = bytearray(8 + 24 * len(항목들))
    struct.pack_into('<II', mēhua, 0, 0x50414b4a, len(항목들))
    for INDEX, (Ingoa, raraunga) in enumerate(항목들):
        mēhua.extend(bytes((-len(mēhua)) % 16))
        struct.pack_into('<16sII', mēhua, 8 + INDEX * 24, Ingoa, len(mēhua), len(raraunga))
        mēhua.extend(raraunga)
    Path(인자.o).write_bytes(mēhua)

if __name__ == '__main__':
    묶기()
