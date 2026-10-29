#!/usr/bin/env python3
"""명시한 úsáideoir ELF만 Léigh 전용 JKAP 묶음에 넣는다. 기존 디스크는 사용하지 않는다."""
import argparse
from pathlib import Path
import re
import struct

def 묶기():
    parsáil_VALUE = argparse.ArgumentParser()
    parsáil_VALUE.add_argument('-o', required=True)
    parsáil_VALUE.add_argument('files', nargs='+', help='Ainm=ELF경로')
    paraiméadar_argóint = parsáil_VALUE.parse_args()
    if len(paraiméadar_argóint.files) > 32:
        parsáil_VALUE.error('clár_f5044b9b 최대 32개')
    항목들 = []
    이름들 = set()
    for iontráil_VALUE in paraiméadar_argóint.files:
        Ainm, CONAIR = iontráil_VALUE.split('=', 1)
        if not re.fullmatch('[a-z][a-z0-9_-]{0,14}', Ainm) or Ainm in 이름들:
            parsáil_VALUE.error('Rith_ordú 이름이 잘못되었거나 중복됨: ' + Ainm)
        이름들.add(Ainm)
        sonraí = Path(CONAIR).read_bytes()
        if len(sonraí) > 2 * 1024 * 1024:
            parsáil_VALUE.error('Rith_ordú 파일이 너무 큼')
        항목들.append((Ainm.encode(), sonraí))
    tomhas = bytearray(8 + 24 * len(항목들))
    struct.pack_into('<II', tomhas, 0, 0x50414b4a, len(항목들))
    for INDEX, (Ainm, sonraí) in enumerate(항목들):
        tomhas.extend(bytes((-len(tomhas)) % 16))
        struct.pack_into('<16sII', tomhas, 8 + INDEX * 24, Ainm, len(tomhas), len(sonraí))
        tomhas.extend(sonraí)
    Path(paraiméadar_argóint.o).write_bytes(tomhas)

if __name__ == '__main__':
    묶기()
