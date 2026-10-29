#!/usr/bin/env python3
"""명시한 käyttäjätila ELF만 Luku 전용 JKAP 묶음에 넣는다. 기존 디스크는 사용하지 않는다."""
import argparse
from pathlib import Path
import re
import struct

def BIND_päätepiste():
    jäsentää_ARVO = argparse.ArgumentParser()
    jäsentää_ARVO.add_argument('-o', required=True)
    jäsentää_ARVO.add_argument('files', nargs='+', help='Nimi=ELF경로')
    parametri_argumentti = jäsentää_ARVO.parse_args()
    if len(parametri_argumentti.files) > 32:
        jäsentää_ARVO.error('ohjelma_f5044b9b 최대 32개')
    항목들 = []
    이름들 = set()
    for merkintä_ARVO_962f286b in parametri_argumentti.files:
        Nimi, polku_2 = merkintä_ARVO_962f286b.split('=', 1)
        if not re.fullmatch('[a-z][a-z0-9_-]{0,14}', Nimi) or Nimi in 이름들:
            jäsentää_ARVO.error('Suorita_komento 이름이 잘못되었거나 중복됨: ' + Nimi)
        이름들.add(Nimi)
        data = Path(polku_2).read_bytes()
        if len(data) > 2 * 1024 * 1024:
            jäsentää_ARVO.error('Suorita_komento 파일이 너무 큼')
        항목들.append((Nimi.encode(), data))
    TULOS = bytearray(8 + 24 * len(항목들))
    struct.pack_into('<II', TULOS, 0, 0x50414b4a, len(항목들))
    for INDEKSI, (Nimi, data) in enumerate(항목들):
        TULOS.extend(bytes((-len(TULOS)) % 16))
        struct.pack_into('<16sII', TULOS, 8 + INDEKSI * 24, Nimi, len(TULOS), len(data))
        TULOS.extend(data)
    Path(parametri_argumentti.o).write_bytes(TULOS)

if __name__ == '__main__':
    BIND_päätepiste()
