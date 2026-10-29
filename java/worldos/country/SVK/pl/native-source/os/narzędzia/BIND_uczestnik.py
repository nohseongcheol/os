#!/usr/bin/env python3
"""명시한 przestrzeń_użytkownika ELF만 Odczyt 전용 JKAP 묶음에 넣는다. 기존 디스크는 사용하지 않는다."""
import argparse
from pathlib import Path
import re
import struct

def BIND_uczestnik():
    analizować_WARTOŚĆ = argparse.ArgumentParser()
    analizować_WARTOŚĆ.add_argument('-o', required=True)
    analizować_WARTOŚĆ.add_argument('files', nargs='+', help='Nazwa=ELF경로')
    parametr_argument = analizować_WARTOŚĆ.parse_args()
    if len(parametr_argument.files) > 32:
        analizować_WARTOŚĆ.error('program_f5044b9b 최대 32개')
    항목들 = []
    이름들 = set()
    for wpis_WARTOŚĆ in parametr_argument.files:
        Nazwa, ścieżka_2 = wpis_WARTOŚĆ.split('=', 1)
        if not re.fullmatch('[a-z][a-z0-9_-]{0,14}', Nazwa) or Nazwa in 이름들:
            analizować_WARTOŚĆ.error('Wykonaj_polecenie 이름이 잘못되었거나 중복됨: ' + Nazwa)
        이름들.add(Nazwa)
        dane = Path(ścieżka_2).read_bytes()
        if len(dane) > 2 * 1024 * 1024:
            analizować_WARTOŚĆ.error('Wykonaj_polecenie 파일이 너무 큼')
        항목들.append((Nazwa.encode(), dane))
    WYNIK = bytearray(8 + 24 * len(항목들))
    struct.pack_into('<II', WYNIK, 0, 0x50414b4a, len(항목들))
    for INDEKS, (Nazwa, dane) in enumerate(항목들):
        WYNIK.extend(bytes((-len(WYNIK)) % 16))
        struct.pack_into('<16sII', WYNIK, 8 + INDEKS * 24, Nazwa, len(WYNIK), len(dane))
        WYNIK.extend(dane)
    Path(parametr_argument.o).write_bytes(WYNIK)

if __name__ == '__main__':
    BIND_uczestnik()
