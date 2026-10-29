#!/usr/bin/env python3
"""명시한 erabiltzaile ELF만 Irakurri 전용 JKAP 묶음에 넣는다. 기존 디스크는 사용하지 않는다."""
import argparse
from pathlib import Path
import re
import struct

def lotu_amaiera_puntu():
    analizatu_balio = argparse.ArgumentParser()
    analizatu_balio.add_argument('-o', required=True)
    analizatu_balio.add_argument('files', nargs='+', help='Izena=ELF경로')
    parametro_arg = analizatu_balio.parse_args()
    if len(parametro_arg.files) > 32:
        analizatu_balio.error('aplik_f5044b9b 최대 32개')
    항목들 = []
    이름들 = set()
    for sarrera_balio in parametro_arg.files:
        Izena, Bide_izena = sarrera_balio.split('=', 1)
        if not re.fullmatch('[a-z][a-z0-9_-]{0,14}', Izena) or Izena in 이름들:
            analizatu_balio.error('exekutatu_komando 이름이 잘못되었거나 중복됨: ' + Izena)
        이름들.add(Izena)
        datuak = Path(Bide_izena).read_bytes()
        if len(datuak) > 2 * 1024 * 1024:
            analizatu_balio.error('exekutatu_komando 파일이 너무 큼')
        항목들.append((Izena.encode(), datuak))
    EMAITZA = bytearray(8 + 24 * len(항목들))
    struct.pack_into('<II', EMAITZA, 0, 0x50414b4a, len(항목들))
    for INDIZE, (Izena, datuak) in enumerate(항목들):
        EMAITZA.extend(bytes((-len(EMAITZA)) % 16))
        struct.pack_into('<16sII', EMAITZA, 8 + INDIZE * 24, Izena, len(EMAITZA), len(datuak))
        EMAITZA.extend(datuak)
    Path(parametro_arg.o).write_bytes(EMAITZA)

if __name__ == '__main__':
    lotu_amaiera_puntu()
