#!/usr/bin/env python3
"""새 파일에만 JKSTORE1 전용 Store_VALUE 매체를 만든다. 기존 Fajl/장치는 덮어쓰지 않는다."""
import argparse
from pathlib import Path
import struct

def Create_unos(Putanja):
    with Path(Putanja).open('xb') as Ispis:
        머리 = bytearray(512)
        struct.pack_into('<8sII', 머리, 0, b'JKSTORE1', 2048, 0x3153464a)
        Ispis.write(머리)
        Ispis.truncate(2048 * 512)

if __name__ == '__main__':
    해석기 = argparse.ArgumentParser(description=__doc__)
    해석기.add_argument('Putanja')
    Argumenti = 해석기.parse_args()
    Create_unos(Argumenti.Putanja)
