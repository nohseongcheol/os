#!/usr/bin/env python3
"""명시한 korisnik ELF만 읽기 전용 JKAP 묶음에 넣는다. 기존 디스크는 사용하지 않는다."""
import argparse
from pathlib import Path
import re
import struct

def povezati_učesnik():
    raščlaniti_VALUE = argparse.ArgumentParser()
    raščlaniti_VALUE.add_argument('-o', required=True)
    raščlaniti_VALUE.add_argument('files', nargs='+', help='ime=ELF경로')
    parametar_argument = raščlaniti_VALUE.parse_args()
    if len(parametar_argument.files) > 32:
        raščlaniti_VALUE.error('program_f5044b9b 최대 32개')
    항목들 = []
    이름들 = set()
    for stavka_VALUE in parametar_argument.files:
        ime, putanja = stavka_VALUE.split('=', 1)
        if not re.fullmatch('[a-z][a-z0-9_-]{0,14}', ime) or ime in 이름들:
            raščlaniti_VALUE.error('Izvrši_komanda 이름이 잘못되었거나 중복됨: ' + ime)
        이름들.add(ime)
        podaci = Path(putanja).read_bytes()
        if len(podaci) > 2 * 1024 * 1024:
            raščlaniti_VALUE.error('Izvrši_komanda 파일이 너무 큼')
        항목들.append((ime.encode(), podaci))
    KR = bytearray(8 + 24 * len(항목들))
    struct.pack_into('<II', KR, 0, 0x50414b4a, len(항목들))
    for INDEX, (ime, podaci) in enumerate(항목들):
        KR.extend(bytes((-len(KR)) % 16))
        struct.pack_into('<16sII', KR, 8 + INDEX * 24, ime, len(KR), len(podaci))
        KR.extend(podaci)
    Path(parametar_argument.o).write_bytes(KR)

if __name__ == '__main__':
    povezati_učesnik()
