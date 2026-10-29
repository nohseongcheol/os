#!/usr/bin/env python3
"""명시한 uporabnik ELF만 Branje 전용 JKAP 묶음에 넣는다. 기존 디스크는 사용하지 않는다."""
import argparse
from pathlib import Path
import re
import struct

def BIND_končna_točka():
    razčlenjevati_VALUE = argparse.ArgumentParser()
    razčlenjevati_VALUE.add_argument('-o', required=True)
    razčlenjevati_VALUE.add_argument('files', nargs='+', help='Ime=ELF경로')
    parameter_argument = razčlenjevati_VALUE.parse_args()
    if len(parameter_argument.files) > 32:
        razčlenjevati_VALUE.error('aplikacija_f5044b9b 최대 32개')
    항목들 = []
    이름들 = set()
    for vnos_VALUE in parameter_argument.files:
        Ime, POT = vnos_VALUE.split('=', 1)
        if not re.fullmatch('[a-z][a-z0-9_-]{0,14}', Ime) or Ime in 이름들:
            razčlenjevati_VALUE.error('Izvedi_ukaz 이름이 잘못되었거나 중복됨: ' + Ime)
        이름들.add(Ime)
        podatki = Path(POT).read_bytes()
        if len(podatki) > 2 * 1024 * 1024:
            razčlenjevati_VALUE.error('Izvedi_ukaz 파일이 너무 큼')
        항목들.append((Ime.encode(), podatki))
    REZULTAT = bytearray(8 + 24 * len(항목들))
    struct.pack_into('<II', REZULTAT, 0, 0x50414b4a, len(항목들))
    for INDEX, (Ime, podatki) in enumerate(항목들):
        REZULTAT.extend(bytes((-len(REZULTAT)) % 16))
        struct.pack_into('<16sII', REZULTAT, 8 + INDEX * 24, Ime, len(REZULTAT), len(podatki))
        REZULTAT.extend(podatki)
    Path(parameter_argument.o).write_bytes(REZULTAT)

if __name__ == '__main__':
    BIND_končna_točka()
