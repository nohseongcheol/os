#!/usr/bin/env python3
"""새 파일에만 JKSTORE1 전용 Store_värde 매체를 만든다. 기존 filnamn/장치는 덮어쓰지 않는다."""
import argparse
from pathlib import Path
import struct

def Skapa_post(sökväg_2):
    with Path(sökväg_2).open('xb') as utmatningsposition:
        머리 = bytearray(512)
        struct.pack_into('<8sII', 머리, 0, b'JKSTORE1', 2048, 0x3153464a)
        utmatningsposition.write(머리)
        utmatningsposition.truncate(2048 * 512)

if __name__ == '__main__':
    parser_48ee4b1b = argparse.ArgumentParser(description=__doc__)
    parser_48ee4b1b.add_argument('sökväg_2')
    argument = parser_48ee4b1b.parse_args()
    Skapa_post(argument.sökväg_2)
