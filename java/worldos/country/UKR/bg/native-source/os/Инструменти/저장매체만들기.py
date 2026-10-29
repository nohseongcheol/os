#!/usr/bin/env python3
"""새 파일에만 JKSTORE1 전용 хранилище_стойност 매체를 만든다. 기존 Файл/장치는 덮어쓰지 않는다."""
import argparse
from pathlib import Path
import struct

def Създаване_запис(ПЪТ):
    with Path(ПЪТ).open('xb') as Изход:
        머리 = bytearray(512)
        struct.pack_into('<8sII', 머리, 0, b'JKSTORE1', 2048, 0x3153464a)
        Изход.write(머리)
        Изход.truncate(2048 * 512)

if __name__ == '__main__':
    анализатор_48ee4b1b = argparse.ArgumentParser(description=__doc__)
    анализатор_48ee4b1b.add_argument('ПЪТ')
    Параметри = анализатор_48ee4b1b.parse_args()
    Създаване_запис(Параметри.ПЪТ)
