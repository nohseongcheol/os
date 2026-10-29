#!/usr/bin/env python3
"""명시한 사용자 ELF만 Чита 전용 JKAP 묶음에 넣는다. 기존 디스크는 사용하지 않는다."""
import argparse
from pathlib import Path
import re
import struct

def 묶기():
    해석 = argparse.ArgumentParser()
    해석.add_argument('-o', required=True)
    해석.add_argument('files', nargs='+', help='Назив=ELF경로')
    인자 = 해석.parse_args()
    if len(인자.files) > 32:
        해석.error('프로그램 최대 32개')
    항목들 = []
    이름들 = set()
    for 항목 in 인자.files:
        Назив, ПУТАЊА = 항목.split('=', 1)
        if not re.fullmatch('[a-z][a-z0-9_-]{0,14}', Назив) or Назив in 이름들:
            해석.error('실행 이름이 잘못되었거나 중복됨: ' + Назив)
        이름들.add(Назив)
        자료 = Path(ПУТАЊА).read_bytes()
        if len(자료) > 2 * 1024 * 1024:
            해석.error('실행 파일이 너무 큼')
        항목들.append((Назив.encode(), 자료))
    ИСХОД = bytearray(8 + 24 * len(항목들))
    struct.pack_into('<II', ИСХОД, 0, 0x50414b4a, len(항목들))
    for 번호, (Назив, 자료) in enumerate(항목들):
        ИСХОД.extend(bytes((-len(ИСХОД)) % 16))
        struct.pack_into('<16sII', ИСХОД, 8 + 번호 * 24, Назив, len(ИСХОД), len(자료))
        ИСХОД.extend(자료)
    Path(인자.o).write_bytes(ИСХОД)

if __name__ == '__main__':
    묶기()
