#!/usr/bin/env python3
"""명시한 корисник ELF만 Чита 전용 JKAP 묶음에 넣는다. 기존 디스크는 사용하지 않는다."""
import argparse
from pathlib import Path
import re
import struct

def повезати_крајња_тачка():
    рашчланити_вриједност = argparse.ArgumentParser()
    рашчланити_вриједност.add_argument('-o', required=True)
    рашчланити_вриједност.add_argument('files', nargs='+', help='Назив=ELF경로')
    параметар_аргумент = рашчланити_вриједност.parse_args()
    if len(параметар_аргумент.files) > 32:
        рашчланити_вриједност.error('програм_f5044b9b 최대 32개')
    항목들 = []
    이름들 = set()
    for унос_вриједност in параметар_аргумент.files:
        Назив, ПУТАЊА = унос_вриједност.split('=', 1)
        if not re.fullmatch('[a-z][a-z0-9_-]{0,14}', Назив) or Назив in 이름들:
            рашчланити_вриједност.error('Изврши_команда 이름이 잘못되었거나 중복됨: ' + Назив)
        이름들.add(Назив)
        подаци = Path(ПУТАЊА).read_bytes()
        if len(подаци) > 2 * 1024 * 1024:
            рашчланити_вриједност.error('Изврши_команда 파일이 너무 큼')
        항목들.append((Назив.encode(), подаци))
    ИСХОД = bytearray(8 + 24 * len(항목들))
    struct.pack_into('<II', ИСХОД, 0, 0x50414b4a, len(항목들))
    for индекс, (Назив, подаци) in enumerate(항목들):
        ИСХОД.extend(bytes((-len(ИСХОД)) % 16))
        struct.pack_into('<16sII', ИСХОД, 8 + индекс * 24, Назив, len(ИСХОД), len(подаци))
        ИСХОД.extend(подаци)
    Path(параметар_аргумент.o).write_bytes(ИСХОД)

if __name__ == '__main__':
    повезати_крајња_тачка()
