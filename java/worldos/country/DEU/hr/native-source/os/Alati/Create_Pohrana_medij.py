#!/usr/bin/env python3
"""새 파일에만 JKSTORE1 전용 Store_VALUE 매체를 만든다. 기존 Datoteka/장치는 덮어쓰지 않는다."""
import argparse
from pathlib import Path
import struct

def Create_unos(PUTANJA):
    with Path(PUTANJA).open('xb') as Izlaz:
        머리 = bytearray(512)
        struct.pack_into('<8sII', 머리, 0, b'JKSTORE1', 2048, 0x3153464a)
        Izlaz.write(머리)
        Izlaz.truncate(2048 * 512)

if __name__ == '__main__':
    analizator_48ee4b1b = argparse.ArgumentParser(description=__doc__)
    analizator_48ee4b1b.add_argument('PUTANJA')
    Argumenti = analizator_48ee4b1b.parse_args()
    Create_unos(Argumenti.PUTANJA)
