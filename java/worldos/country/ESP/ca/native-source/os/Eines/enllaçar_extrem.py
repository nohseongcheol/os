#!/usr/bin/env python3
"""명시한 usuari ELF만 Lectura 전용 JKAP 묶음에 넣는다. 기존 디스크는 사용하지 않는다."""
import argparse
from pathlib import Path
import re
import struct

def enllaçar_extrem():
    analitzar_VALOR = argparse.ArgumentParser()
    analitzar_VALOR.add_argument('-o', required=True)
    analitzar_VALOR.add_argument('files', nargs='+', help='Nom=ELF경로')
    paràmetre_arg = analitzar_VALOR.parse_args()
    if len(paràmetre_arg.files) > 32:
        analitzar_VALOR.error('programa_f5044b9b 최대 32개')
    항목들 = []
    이름들 = set()
    for introducció_VALOR in paràmetre_arg.files:
        Nom, Camí = introducció_VALOR.split('=', 1)
        if not re.fullmatch('[a-z][a-z0-9_-]{0,14}', Nom) or Nom in 이름들:
            analitzar_VALOR.error('Executa_ordre 이름이 잘못되었거나 중복됨: ' + Nom)
        이름들.add(Nom)
        dades = Path(Camí).read_bytes()
        if len(dades) > 2 * 1024 * 1024:
            analitzar_VALOR.error('Executa_ordre 파일이 너무 큼')
        항목들.append((Nom.encode(), dades))
    RESULTAT = bytearray(8 + 24 * len(항목들))
    struct.pack_into('<II', RESULTAT, 0, 0x50414b4a, len(항목들))
    for INDEX, (Nom, dades) in enumerate(항목들):
        RESULTAT.extend(bytes((-len(RESULTAT)) % 16))
        struct.pack_into('<16sII', RESULTAT, 8 + INDEX * 24, Nom, len(RESULTAT), len(dades))
        RESULTAT.extend(dades)
    Path(paràmetre_arg.o).write_bytes(RESULTAT)

if __name__ == '__main__':
    enllaçar_extrem()
