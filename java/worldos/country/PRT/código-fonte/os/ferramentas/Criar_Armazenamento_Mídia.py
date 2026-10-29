#!/usr/bin/env python3
"""새 파일에만 JKSTORE1 전용 Store_VALOR 매체를 만든다. 기존 ficheiro/장치는 덮어쓰지 않는다."""
import argparse
from pathlib import Path
import struct

def Criar_entrada(caminho):
    with Path(caminho).open('xb') as saídaTexto:
        HEAD_VALOR = bytearray(512)
        struct.pack_into('<8sII', HEAD_VALOR, 0, b'JKSTORE1', 2048, 0x3153464a)
        saídaTexto.write(HEAD_VALOR)
        saídaTexto.truncate(2048 * 512)

if __name__ == '__main__':
    analisador_48ee4b1b = argparse.ArgumentParser(description=__doc__)
    analisador_48ee4b1b.add_argument('caminho')
    argumentos = analisador_48ee4b1b.parse_args()
    Criar_entrada(argumentos.caminho)
