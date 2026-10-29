#!/usr/bin/env python3
"""명시한 korisnik ELF만 Čitaj 전용 JKAP 묶음에 넣는다. 기존 디스크는 사용하지 않는다."""
import argparse
from pathlib import Path
import re
import struct

def BIND_sudionik():
    rastavljati_VALUE = argparse.ArgumentParser()
    rastavljati_VALUE.add_argument('-o', required=True)
    rastavljati_VALUE.add_argument('files', nargs='+', help='Ime=ELF경로')
    parametar_argument = rastavljati_VALUE.parse_args()
    if len(parametar_argument.files) > 32:
        rastavljati_VALUE.error('program_f5044b9b 최대 32개')
    항목들 = []
    이름들 = set()
    for unos_VALUE in parametar_argument.files:
        Ime, PUTANJA = unos_VALUE.split('=', 1)
        if not re.fullmatch('[a-z][a-z0-9_-]{0,14}', Ime) or Ime in 이름들:
            rastavljati_VALUE.error('Izvrši_naredba 이름이 잘못되었거나 중복됨: ' + Ime)
        이름들.add(Ime)
        podaci = Path(PUTANJA).read_bytes()
        if len(podaci) > 2 * 1024 * 1024:
            rastavljati_VALUE.error('Izvrši_naredba 파일이 너무 큼')
        항목들.append((Ime.encode(), podaci))
    REZULTAT = bytearray(8 + 24 * len(항목들))
    struct.pack_into('<II', REZULTAT, 0, 0x50414b4a, len(항목들))
    for INDEX, (Ime, podaci) in enumerate(항목들):
        REZULTAT.extend(bytes((-len(REZULTAT)) % 16))
        struct.pack_into('<16sII', REZULTAT, 8 + INDEX * 24, Ime, len(REZULTAT), len(podaci))
        REZULTAT.extend(podaci)
    Path(parametar_argument.o).write_bytes(REZULTAT)

if __name__ == '__main__':
    BIND_sudionik()
