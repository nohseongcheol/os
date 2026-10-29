#!/usr/bin/env python3
"""새 파일에만 JKSTORE1 전용 Store_VALUE 매체를 만든다. 기존 Datoteka/장치는 덮어쓰지 않는다."""
import argparse
from pathlib import Path
import struct

def Create_stavka(putanja):
    with Path(putanja).open('xb') as 출력:
        머리 = bytearray(512)
        struct.pack_into('<8sII', 머리, 0, b'JKSTORE1', 2048, 0x3153464a)
        출력.write(머리)
        출력.truncate(2048 * 512)

if __name__ == '__main__':
    analizator_48ee4b1b = argparse.ArgumentParser(description=__doc__)
    analizator_48ee4b1b.add_argument('putanja')
    인수 = analizator_48ee4b1b.parse_args()
    Create_stavka(인수.putanja)
