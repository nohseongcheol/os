#!/usr/bin/env python3
"""명시한 espaço_do_utilizador ELF만 Leitura 전용 JKAP 묶음에 넣는다. 기존 디스크는 사용하지 않는다."""
import argparse
from pathlib import Path
import re
import struct

def BIND_empresa():
    analisar_VALOR = argparse.ArgumentParser()
    analisar_VALOR.add_argument('-o', required=True)
    analisar_VALOR.add_argument('files', nargs='+', help='Nome=ELF경로')
    parâmetro_argumento = analisar_VALOR.parse_args()
    if len(parâmetro_argumento.files) > 32:
        analisar_VALOR.error('app_f5044b9b 최대 32개')
    항목들 = []
    이름들 = set()
    for entrada_VALOR_962f286b in parâmetro_argumento.files:
        Nome, caminho = entrada_VALOR_962f286b.split('=', 1)
        if not re.fullmatch('[a-z][a-z0-9_-]{0,14}', Nome) or Nome in 이름들:
            analisar_VALOR.error('Executar_comando 이름이 잘못되었거나 중복됨: ' + Nome)
        이름들.add(Nome)
        dados = Path(caminho).read_bytes()
        if len(dados) > 2 * 1024 * 1024:
            analisar_VALOR.error('Executar_comando 파일이 너무 큼')
        항목들.append((Nome.encode(), dados))
    resultado = bytearray(8 + 24 * len(항목들))
    struct.pack_into('<II', resultado, 0, 0x50414b4a, len(항목들))
    for ÍNDICE, (Nome, dados) in enumerate(항목들):
        resultado.extend(bytes((-len(resultado)) % 16))
        struct.pack_into('<16sII', resultado, 8 + ÍNDICE * 24, Nome, len(resultado), len(dados))
        resultado.extend(dados)
    Path(parâmetro_argumento.o).write_bytes(resultado)

if __name__ == '__main__':
    BIND_empresa()
