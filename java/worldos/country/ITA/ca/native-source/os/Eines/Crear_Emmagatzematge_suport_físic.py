#!/usr/bin/env python3
"""새 파일에만 JKSTORE1 전용 Store_VALOR 매체를 만든다. 기존 Fitxer/장치는 덮어쓰지 않는다."""
import argparse
from pathlib import Path
import struct

def Crear_introducció(Camí):
    with Path(Camí).open('xb') as Sortida:
        머리 = bytearray(512)
        struct.pack_into('<8sII', 머리, 0, b'JKSTORE1', 2048, 0x3153464a)
        Sortida.write(머리)
        Sortida.truncate(2048 * 512)

if __name__ == '__main__':
    analitzador_48ee4b1b = argparse.ArgumentParser(description=__doc__)
    analitzador_48ee4b1b.add_argument('Camí')
    인수 = analitzador_48ee4b1b.parse_args()
    Crear_introducció(인수.Camí)
