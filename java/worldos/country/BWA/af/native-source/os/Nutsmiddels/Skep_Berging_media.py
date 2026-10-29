#!/usr/bin/env python3
"""새 파일에만 JKSTORE1 전용 bêre_VALUE 매체를 만든다. 기존 Lêer/장치는 덮어쓰지 않는다."""
import argparse
from pathlib import Path
import struct

def Skep_inskrywing(Pad):
    with Path(Pad).open('xb') as Afvoer:
        머리 = bytearray(512)
        struct.pack_into('<8sII', 머리, 0, b'JKSTORE1', 2048, 0x3153464a)
        Afvoer.write(머리)
        Afvoer.truncate(2048 * 512)

if __name__ == '__main__':
    ontleder_48ee4b1b = argparse.ArgumentParser(description=__doc__)
    ontleder_48ee4b1b.add_argument('Pad')
    인수 = ontleder_48ee4b1b.parse_args()
    Skep_inskrywing(인수.Pad)
