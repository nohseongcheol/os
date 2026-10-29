#!/usr/bin/env python3
"""명시한 användarutrymme ELF만 Läs 전용 JKAP 묶음에 넣는다. 기존 디스크는 사용하지 않는다."""
import argparse
from pathlib import Path
import re
import struct

def BIND_deltagare():
    parsa_värde = argparse.ArgumentParser()
    parsa_värde.add_argument('-o', required=True)
    parsa_värde.add_argument('files', nargs='+', help='Namn=ELF경로')
    parameter_argument = parsa_värde.parse_args()
    if len(parameter_argument.files) > 32:
        parsa_värde.error('app_f5044b9b 최대 32개')
    항목들 = []
    이름들 = set()
    for post_värde in parameter_argument.files:
        Namn, sökväg_2 = post_värde.split('=', 1)
        if not re.fullmatch('[a-z][a-z0-9_-]{0,14}', Namn) or Namn in 이름들:
            parsa_värde.error('köra_kommando 이름이 잘못되었거나 중복됨: ' + Namn)
        이름들.add(Namn)
        data = Path(sökväg_2).read_bytes()
        if len(data) > 2 * 1024 * 1024:
            parsa_värde.error('köra_kommando 파일이 너무 큼')
        항목들.append((Namn.encode(), data))
    RESULTAT = bytearray(8 + 24 * len(항목들))
    struct.pack_into('<II', RESULTAT, 0, 0x50414b4a, len(항목들))
    for INDEX, (Namn, data) in enumerate(항목들):
        RESULTAT.extend(bytes((-len(RESULTAT)) % 16))
        struct.pack_into('<16sII', RESULTAT, 8 + INDEX * 24, Namn, len(RESULTAT), len(data))
        RESULTAT.extend(data)
    Path(parameter_argument.o).write_bytes(RESULTAT)

if __name__ == '__main__':
    BIND_deltagare()
