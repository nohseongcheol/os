#!/usr/bin/env python3
"""새 파일에만 JKSTORE1 전용 Store_HODNOTA 매체를 만든다. 기존 název_souboru/장치는 덮어쓰지 않는다."""
import argparse
from pathlib import Path
import struct

def Create_položka(cesta_2):
    with Path(cesta_2).open('xb') as výstupní_pozice:
        머리 = bytearray(512)
        struct.pack_into('<8sII', 머리, 0, b'JKSTORE1', 2048, 0x3153464a)
        výstupní_pozice.write(머리)
        výstupní_pozice.truncate(2048 * 512)

if __name__ == '__main__':
    analyzátor_48ee4b1b = argparse.ArgumentParser(description=__doc__)
    analyzátor_48ee4b1b.add_argument('cesta_2')
    argumenty = analyzátor_48ee4b1b.parse_args()
    Create_položka(argumenty.cesta_2)
