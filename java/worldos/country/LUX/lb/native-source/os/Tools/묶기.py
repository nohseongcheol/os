#!/usr/bin/env python3
"""명시한 Benotzer ELF만 읽기 전용 JKAP 묶음에 넣는다. 기존 디스크는 사용하지 않는다."""
import argparse
from pathlib import Path
import re
import struct

def 묶기():
    analyséieren_VALUE = argparse.ArgumentParser()
    analyséieren_VALUE.add_argument('-o', required=True)
    analyséieren_VALUE.add_argument('files', nargs='+', help='Numm=ELF경로')
    인자 = analyséieren_VALUE.parse_args()
    if len(인자.files) > 32:
        analyséieren_VALUE.error('App_f5044b9b 최대 32개')
    항목들 = []
    이름들 = set()
    for Agab_VALUE in 인자.files:
        Numm, Wee = Agab_VALUE.split('=', 1)
        if not re.fullmatch('[a-z][a-z0-9_-]{0,14}', Numm) or Numm in 이름들:
            analyséieren_VALUE.error('ausféieren_Befeel 이름이 잘못되었거나 중복됨: ' + Numm)
        이름들.add(Numm)
        Daten = Path(Wee).read_bytes()
        if len(Daten) > 2 * 1024 * 1024:
            analyséieren_VALUE.error('ausféieren_Befeel 파일이 너무 큼')
        항목들.append((Numm.encode(), Daten))
    Mooss = bytearray(8 + 24 * len(항목들))
    struct.pack_into('<II', Mooss, 0, 0x50414b4a, len(항목들))
    for INDEX, (Numm, Daten) in enumerate(항목들):
        Mooss.extend(bytes((-len(Mooss)) % 16))
        struct.pack_into('<16sII', Mooss, 8 + INDEX * 24, Numm, len(Mooss), len(Daten))
        Mooss.extend(Daten)
    Path(인자.o).write_bytes(Mooss)

if __name__ == '__main__':
    묶기()
