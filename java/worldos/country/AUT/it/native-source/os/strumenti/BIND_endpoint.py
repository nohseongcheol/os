#!/usr/bin/env python3
"""명시한 spazio_utente ELF만 Lettura 전용 JKAP 묶음에 넣는다. 기존 디스크는 사용하지 않는다."""
import argparse
from pathlib import Path
import re
import struct

def BIND_endpoint():
    analizzare_VALORE = argparse.ArgumentParser()
    analizzare_VALORE.add_argument('-o', required=True)
    analizzare_VALORE.add_argument('files', nargs='+', help='Nome=ELF경로')
    parametro_argomento = analizzare_VALORE.parse_args()
    if len(parametro_argomento.files) > 32:
        analizzare_VALORE.error('app_f5044b9b 최대 32개')
    항목들 = []
    이름들 = set()
    for voce_VALORE in parametro_argomento.files:
        Nome, percorso = voce_VALORE.split('=', 1)
        if not re.fullmatch('[a-z][a-z0-9_-]{0,14}', Nome) or Nome in 이름들:
            analizzare_VALORE.error('Esegui_comando 이름이 잘못되었거나 중복됨: ' + Nome)
        이름들.add(Nome)
        dati = Path(percorso).read_bytes()
        if len(dati) > 2 * 1024 * 1024:
            analizzare_VALORE.error('Esegui_comando 파일이 너무 큼')
        항목들.append((Nome.encode(), dati))
    risultato = bytearray(8 + 24 * len(항목들))
    struct.pack_into('<II', risultato, 0, 0x50414b4a, len(항목들))
    for INDICE, (Nome, dati) in enumerate(항목들):
        risultato.extend(bytes((-len(risultato)) % 16))
        struct.pack_into('<16sII', risultato, 8 + INDICE * 24, Nome, len(risultato), len(dati))
        risultato.extend(dati)
    Path(parametro_argomento.o).write_bytes(risultato)

if __name__ == '__main__':
    BIND_endpoint()
