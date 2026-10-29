#!/usr/bin/env python3
"""새 파일에만 JKSTORE1 전용 Store_VALUE 매체를 만든다. 기존 Skrá/장치는 덮어쓰지 않는다."""
import argparse
from pathlib import Path
import struct

def stofna_færsla(SLÓÐ):
    with Path(SLÓÐ).open('xb') as úttak:
        머리 = bytearray(512)
        struct.pack_into('<8sII', 머리, 0, b'JKSTORE1', 2048, 0x3153464a)
        úttak.write(머리)
        úttak.truncate(2048 * 512)

if __name__ == '__main__':
    þáttari_48ee4b1b = argparse.ArgumentParser(description=__doc__)
    þáttari_48ee4b1b.add_argument('SLÓÐ')
    Viðföng = þáttari_48ee4b1b.parse_args()
    stofna_færsla(Viðföng.SLÓÐ)
