#!/usr/bin/env python3
"""명시한 naudotojas ELF만 Skaitymas 전용 JKAP 묶음에 넣는다. 기존 디스크는 사용하지 않는다."""
import argparse
from pathlib import Path
import re
import struct

def BIND_dalyvis():
    analizuoti_sintaksę_VALUE = argparse.ArgumentParser()
    analizuoti_sintaksę_VALUE.add_argument('-o', required=True)
    analizuoti_sintaksę_VALUE.add_argument('files', nargs='+', help='Pavadinimas_2=ELF경로')
    parametras_argumentas = analizuoti_sintaksę_VALUE.parse_args()
    if len(parametras_argumentas.files) > 32:
        analizuoti_sintaksę_VALUE.error('programa_f5044b9b 최대 32개')
    항목들 = []
    이름들 = set()
    for įrašas_VALUE in parametras_argumentas.files:
        Pavadinimas_2, KELIAS = įrašas_VALUE.split('=', 1)
        if not re.fullmatch('[a-z][a-z0-9_-]{0,14}', Pavadinimas_2) or Pavadinimas_2 in 이름들:
            analizuoti_sintaksę_VALUE.error('Vykdyti_komanda 이름이 잘못되었거나 중복됨: ' + Pavadinimas_2)
        이름들.add(Pavadinimas_2)
        duomenys = Path(KELIAS).read_bytes()
        if len(duomenys) > 2 * 1024 * 1024:
            analizuoti_sintaksę_VALUE.error('Vykdyti_komanda 파일이 너무 큼')
        항목들.append((Pavadinimas_2.encode(), duomenys))
    REZULTATAS = bytearray(8 + 24 * len(항목들))
    struct.pack_into('<II', REZULTATAS, 0, 0x50414b4a, len(항목들))
    for INDEX, (Pavadinimas_2, duomenys) in enumerate(항목들):
        REZULTATAS.extend(bytes((-len(REZULTATAS)) % 16))
        struct.pack_into('<16sII', REZULTATAS, 8 + INDEX * 24, Pavadinimas_2, len(REZULTATAS), len(duomenys))
        REZULTATAS.extend(duomenys)
    Path(parametras_argumentas.o).write_bytes(REZULTATAS)

if __name__ == '__main__':
    BIND_dalyvis()
