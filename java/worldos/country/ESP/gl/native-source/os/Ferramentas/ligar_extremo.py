#!/usr/bin/env python3
"""명시한 usuario ELF만 Lectura 전용 JKAP 묶음에 넣는다. 기존 디스크는 사용하지 않는다."""
import argparse
from pathlib import Path
import re
import struct

def ligar_extremo():
    analizar_VALOR = argparse.ArgumentParser()
    analizar_VALOR.add_argument('-o', required=True)
    analizar_VALOR.add_argument('files', nargs='+', help='Nome=ELF경로')
    parámetro_argumento = analizar_VALOR.parse_args()
    if len(parámetro_argumento.files) > 32:
        analizar_VALOR.error('apl_f5044b9b 최대 32개')
    항목들 = []
    이름들 = set()
    for introdución_VALOR in parámetro_argumento.files:
        Nome, CAMIÑO = introdución_VALOR.split('=', 1)
        if not re.fullmatch('[a-z][a-z0-9_-]{0,14}', Nome) or Nome in 이름들:
            analizar_VALOR.error('executar_comando 이름이 잘못되었거나 중복됨: ' + Nome)
        이름들.add(Nome)
        datos = Path(CAMIÑO).read_bytes()
        if len(datos) > 2 * 1024 * 1024:
            analizar_VALOR.error('executar_comando 파일이 너무 큼')
        항목들.append((Nome.encode(), datos))
    RESULTANTE = bytearray(8 + 24 * len(항목들))
    struct.pack_into('<II', RESULTANTE, 0, 0x50414b4a, len(항목들))
    for ÍNDICE, (Nome, datos) in enumerate(항목들):
        RESULTANTE.extend(bytes((-len(RESULTANTE)) % 16))
        struct.pack_into('<16sII', RESULTANTE, 8 + ÍNDICE * 24, Nome, len(RESULTANTE), len(datos))
        RESULTANTE.extend(datos)
    Path(parámetro_argumento.o).write_bytes(RESULTANTE)

if __name__ == '__main__':
    ligar_extremo()
