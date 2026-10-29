#!/usr/bin/env python3
"""명시한 uživatelský_prostor ELF만 Čtení 전용 JKAP 묶음에 넣는다. 기존 디스크는 사용하지 않는다."""
import argparse
from pathlib import Path
import re
import struct

def vázat_účastník():
    parsovat_HODNOTA = argparse.ArgumentParser()
    parsovat_HODNOTA.add_argument('-o', required=True)
    parsovat_HODNOTA.add_argument('files', nargs='+', help='Název=ELF경로')
    parametr_argument = parsovat_HODNOTA.parse_args()
    if len(parametr_argument.files) > 32:
        parsovat_HODNOTA.error('program_f5044b9b 최대 32개')
    항목들 = []
    이름들 = set()
    for položka_HODNOTA in parametr_argument.files:
        Název, cesta_2 = položka_HODNOTA.split('=', 1)
        if not re.fullmatch('[a-z][a-z0-9_-]{0,14}', Název) or Název in 이름들:
            parsovat_HODNOTA.error('Provést_příkaz 이름이 잘못되었거나 중복됨: ' + Název)
        이름들.add(Název)
        data = Path(cesta_2).read_bytes()
        if len(data) > 2 * 1024 * 1024:
            parsovat_HODNOTA.error('Provést_příkaz 파일이 너무 큼')
        항목들.append((Název.encode(), data))
    VÝSLEDEK = bytearray(8 + 24 * len(항목들))
    struct.pack_into('<II', VÝSLEDEK, 0, 0x50414b4a, len(항목들))
    for INDEX, (Název, data) in enumerate(항목들):
        VÝSLEDEK.extend(bytes((-len(VÝSLEDEK)) % 16))
        struct.pack_into('<16sII', VÝSLEDEK, 8 + INDEX * 24, Název, len(VÝSLEDEK), len(data))
        VÝSLEDEK.extend(data)
    Path(parametr_argument.o).write_bytes(VÝSLEDEK)

if __name__ == '__main__':
    vázat_účastník()
