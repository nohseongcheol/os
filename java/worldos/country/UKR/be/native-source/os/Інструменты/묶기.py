#!/usr/bin/env python3
"""명시한 карыстальнік ELF만 Чытанне 전용 JKAP 묶음에 넣는다. 기존 디스크는 사용하지 않는다."""
import argparse
from pathlib import Path
import re
import struct

def 묶기():
    해석 = argparse.ArgumentParser()
    해석.add_argument('-o', required=True)
    해석.add_argument('files', nargs='+', help='Назва=ELF경로')
    параметр_аргумент = 해석.parse_args()
    if len(параметр_аргумент.files) > 32:
        해석.error('праграма_f5044b9b 최대 32개')
    항목들 = []
    이름들 = set()
    for увядзенне_значэнне in параметр_аргумент.files:
        Назва, ШЛЯХ = увядзенне_значэнне.split('=', 1)
        if not re.fullmatch('[a-z][a-z0-9_-]{0,14}', Назва) or Назва in 이름들:
            해석.error('выканаць_каманда 이름이 잘못되었거나 중복됨: ' + Назва)
        이름들.add(Назва)
        дадзеныя = Path(ШЛЯХ).read_bytes()
        if len(дадзеныя) > 2 * 1024 * 1024:
            해석.error('выканаць_каманда 파일이 너무 큼')
        항목들.append((Назва.encode(), дадзеныя))
    결과 = bytearray(8 + 24 * len(항목들))
    struct.pack_into('<II', 결과, 0, 0x50414b4a, len(항목들))
    for індэкс, (Назва, дадзеныя) in enumerate(항목들):
        결과.extend(bytes((-len(결과)) % 16))
        struct.pack_into('<16sII', 결과, 8 + індэкс * 24, Назва, len(결과), len(дадзеныя))
        결과.extend(дадзеныя)
    Path(параметр_аргумент.o).write_bytes(결과)

if __name__ == '__main__':
    묶기()
