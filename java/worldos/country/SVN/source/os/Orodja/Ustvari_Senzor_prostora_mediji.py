#!/usr/bin/env python3
"""새 파일에만 JKSTORE1 전용 Store_VALUE 매체를 만든다. 기존 Datoteka/장치는 덮어쓰지 않는다."""
import argparse
from pathlib import Path
import struct

def Ustvari_vnos(POT):
    with Path(POT).open('xb') as Izpis:
        머리 = bytearray(512)
        struct.pack_into('<8sII', 머리, 0, b'JKSTORE1', 2048, 0x3153464a)
        Izpis.write(머리)
        Izpis.truncate(2048 * 512)

if __name__ == '__main__':
    razčlenjevalnik_48ee4b1b = argparse.ArgumentParser(description=__doc__)
    razčlenjevalnik_48ee4b1b.add_argument('POT')
    Argumenti = razčlenjevalnik_48ee4b1b.parse_args()
    Ustvari_vnos(Argumenti.POT)
