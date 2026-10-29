#!/usr/bin/env python3
"""명시한 cleachdaiche ELF만 읽기 전용 JKAP 묶음에 넣는다. 기존 디스크는 사용하지 않는다."""
import argparse
from pathlib import Path
import re
import struct

def 묶기():
    해석 = argparse.ArgumentParser()
    해석.add_argument('-o', required=True)
    해석.add_argument('files', nargs='+', help='Ainm=ELF경로')
    인자 = 해석.parse_args()
    if len(인자.files) > 32:
        해석.error('ap_f5044b9b 최대 32개')
    항목들 = []
    이름들 = set()
    for cur_a_steach_VALUE in 인자.files:
        Ainm, Slighe = cur_a_steach_VALUE.split('=', 1)
        if not re.fullmatch('[a-z][a-z0-9_-]{0,14}', Ainm) or Ainm in 이름들:
            해석.error('gnìomhaich_àithne 이름이 잘못되었거나 중복됨: ' + Ainm)
        이름들.add(Ainm)
        dàta = Path(Slighe).read_bytes()
        if len(dàta) > 2 * 1024 * 1024:
            해석.error('gnìomhaich_àithne 파일이 너무 큼')
        항목들.append((Ainm.encode(), dàta))
    tomhas = bytearray(8 + 24 * len(항목들))
    struct.pack_into('<II', tomhas, 0, 0x50414b4a, len(항목들))
    for INDEX, (Ainm, dàta) in enumerate(항목들):
        tomhas.extend(bytes((-len(tomhas)) % 16))
        struct.pack_into('<16sII', tomhas, 8 + INDEX * 24, Ainm, len(tomhas), len(dàta))
        tomhas.extend(dàta)
    Path(인자.o).write_bytes(tomhas)

if __name__ == '__main__':
    묶기()
