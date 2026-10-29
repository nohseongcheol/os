#!/usr/bin/env python3
"""명시한 utilizator ELF만 Citire 전용 JKAP 묶음에 넣는다. 기존 디스크는 사용하지 않는다."""
import argparse
from pathlib import Path
import re
import struct

def BIND_participant():
    analiza_VALUE = argparse.ArgumentParser()
    analiza_VALUE.add_argument('-o', required=True)
    analiza_VALUE.add_argument('files', nargs='+', help='Nume=ELF경로')
    parametru_argument = analiza_VALUE.parse_args()
    if len(parametru_argument.files) > 32:
        analiza_VALUE.error('program_f5044b9b 최대 32개')
    항목들 = []
    이름들 = set()
    for intrare_VALUE in parametru_argument.files:
        Nume, Cale = intrare_VALUE.split('=', 1)
        if not re.fullmatch('[a-z][a-z0-9_-]{0,14}', Nume) or Nume in 이름들:
            analiza_VALUE.error('executa_comandă 이름이 잘못되었거나 중복됨: ' + Nume)
        이름들.add(Nume)
        date = Path(Cale).read_bytes()
        if len(date) > 2 * 1024 * 1024:
            analiza_VALUE.error('executa_comandă 파일이 너무 큼')
        항목들.append((Nume.encode(), date))
    KR = bytearray(8 + 24 * len(항목들))
    struct.pack_into('<II', KR, 0, 0x50414b4a, len(항목들))
    for INDEX, (Nume, date) in enumerate(항목들):
        KR.extend(bytes((-len(KR)) % 16))
        struct.pack_into('<16sII', KR, 8 + INDEX * 24, Nume, len(KR), len(date))
        KR.extend(date)
    Path(parametru_argument.o).write_bytes(KR)

if __name__ == '__main__':
    BIND_participant()
