#!/usr/bin/env python3
"""새 파일에만 JKSTORE1 전용 сақтау_мән 매체를 만든다. 기존 Файл/장치는 덮어쓰지 않는다."""
import argparse
from pathlib import Path
import struct

def жасау_енгізу(Жол_2):
    with Path(Жол_2).open('xb') as Шығысы:
        머리 = bytearray(512)
        struct.pack_into('<8sII', 머리, 0, b'JKSTORE1', 2048, 0x3153464a)
        Шығысы.write(머리)
        Шығысы.truncate(2048 * 512)

if __name__ == '__main__':
    талдау_құралы_48ee4b1b = argparse.ArgumentParser(description=__doc__)
    талдау_құралы_48ee4b1b.add_argument('Жол_2')
    Аргументтер = талдау_құралы_48ee4b1b.parse_args()
    жасау_енгізу(Аргументтер.Жол_2)
