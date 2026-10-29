#!/usr/bin/env python3
"""새 파일에만 JKSTORE1 전용 Store_balio 매체를 만든다. 기존 Fitxategia/장치는 덮어쓰지 않는다."""
import argparse
from pathlib import Path
import struct

def sortu_sarrera(Bide_izena):
    with Path(Bide_izena).open('xb') as Irteera:
        머리 = bytearray(512)
        struct.pack_into('<8sII', 머리, 0, b'JKSTORE1', 2048, 0x3153464a)
        Irteera.write(머리)
        Irteera.truncate(2048 * 512)

if __name__ == '__main__':
    analizatzaile_48ee4b1b = argparse.ArgumentParser(description=__doc__)
    analizatzaile_48ee4b1b.add_argument('Bide_izena')
    Argumentuak = analizatzaile_48ee4b1b.parse_args()
    sortu_sarrera(Argumentuak.Bide_izena)
