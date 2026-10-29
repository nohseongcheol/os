#!/usr/bin/env python3
"""새 파일에만 JKSTORE1 전용 tár_ÉRTÉK 매체를 만든다. 기존 Fájl/장치는 덮어쓰지 않는다."""
import argparse
from pathlib import Path
import struct

def készít_bejegyzés(ÚTVONAL):
    with Path(ÚTVONAL).open('xb') as Kimenet:
        머리 = bytearray(512)
        struct.pack_into('<8sII', 머리, 0, b'JKSTORE1', 2048, 0x3153464a)
        Kimenet.write(머리)
        Kimenet.truncate(2048 * 512)

if __name__ == '__main__':
    elemző_48ee4b1b = argparse.ArgumentParser(description=__doc__)
    elemző_48ee4b1b.add_argument('ÚTVONAL')
    Argumentumok = elemző_48ee4b1b.parse_args()
    készít_bejegyzés(Argumentumok.ÚTVONAL)
