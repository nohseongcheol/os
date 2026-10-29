#!/usr/bin/env python3
"""명시한 korisnik ELF만 Čitaj 전용 JKAP 묶음에 넣는다. 기존 디스크는 사용하지 않는다."""
import argparse
from pathlib import Path
import re
import struct

def BIND_završna_tačka():
    raščlanjivati_VALUE = argparse.ArgumentParser()
    raščlanjivati_VALUE.add_argument('-o', required=True)
    raščlanjivati_VALUE.add_argument('files', nargs='+', help='Naziv=ELF경로')
    parametar_argument = raščlanjivati_VALUE.parse_args()
    if len(parametar_argument.files) > 32:
        raščlanjivati_VALUE.error('program_f5044b9b 최대 32개')
    항목들 = []
    이름들 = set()
    for unos_VALUE in parametar_argument.files:
        Naziv, Putanja = unos_VALUE.split('=', 1)
        if not re.fullmatch('[a-z][a-z0-9_-]{0,14}', Naziv) or Naziv in 이름들:
            raščlanjivati_VALUE.error('Izvrši_komanda 이름이 잘못되었거나 중복됨: ' + Naziv)
        이름들.add(Naziv)
        podaci = Path(Putanja).read_bytes()
        if len(podaci) > 2 * 1024 * 1024:
            raščlanjivati_VALUE.error('Izvrši_komanda 파일이 너무 큼')
        항목들.append((Naziv.encode(), podaci))
    mjera = bytearray(8 + 24 * len(항목들))
    struct.pack_into('<II', mjera, 0, 0x50414b4a, len(항목들))
    for INDEX, (Naziv, podaci) in enumerate(항목들):
        mjera.extend(bytes((-len(mjera)) % 16))
        struct.pack_into('<16sII', mjera, 8 + INDEX * 24, Naziv, len(mjera), len(podaci))
        mjera.extend(podaci)
    Path(parametar_argument.o).write_bytes(mjera)

if __name__ == '__main__':
    BIND_završna_tačka()
