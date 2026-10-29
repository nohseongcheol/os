#!/usr/bin/env python3
"""새 파일에만 JKSTORE1 전용 Store_VALOR 매체를 만든다. 기존 Ficheiro/장치는 덮어쓰지 않는다."""
import argparse
from pathlib import Path
import struct

def crear_introdución(CAMIÑO):
    with Path(CAMIÑO).open('xb') as Saída:
        머리 = bytearray(512)
        struct.pack_into('<8sII', 머리, 0, b'JKSTORE1', 2048, 0x3153464a)
        Saída.write(머리)
        Saída.truncate(2048 * 512)

if __name__ == '__main__':
    analizador_48ee4b1b = argparse.ArgumentParser(description=__doc__)
    analizador_48ee4b1b.add_argument('CAMIÑO')
    Argumentos = analizador_48ee4b1b.parse_args()
    crear_introdución(Argumentos.CAMIÑO)
