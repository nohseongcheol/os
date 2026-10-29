#!/usr/bin/env python3
"""새 파일에만 JKSTORE1 전용 Store_WARTOŚĆ 매체를 만든다. 기존 nazwa_pliku/장치는 덮어쓰지 않는다."""
import argparse
from pathlib import Path
import struct

def Twórca_wpis(ścieżka_2):
    with Path(ścieżka_2).open('xb') as pozycja_wyjścia:
        머리 = bytearray(512)
        struct.pack_into('<8sII', 머리, 0, b'JKSTORE1', 2048, 0x3153464a)
        pozycja_wyjścia.write(머리)
        pozycja_wyjścia.truncate(2048 * 512)

if __name__ == '__main__':
    parser_48ee4b1b = argparse.ArgumentParser(description=__doc__)
    parser_48ee4b1b.add_argument('ścieżka_2')
    argumenty = parser_48ee4b1b.parse_args()
    Twórca_wpis(argumenty.ścieżka_2)
