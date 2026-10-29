#!/usr/bin/env python3
"""새 파일에만 JKSTORE1 전용 сховище_значення 매체를 만든다. 기존 файл/장치는 덮어쓰지 않는다."""
import argparse
from pathlib import Path
import struct

def Створення_запис(шлях):
    with Path(шлях).open('xb') as Вивід:
        머리 = bytearray(512)
        struct.pack_into('<8sII', 머리, 0, b'JKSTORE1', 2048, 0x3153464a)
        Вивід.write(머리)
        Вивід.truncate(2048 * 512)

if __name__ == '__main__':
    аналізатор_48ee4b1b = argparse.ArgumentParser(description=__doc__)
    аналізатор_48ee4b1b.add_argument('шлях')
    аргументи = аналізатор_48ee4b1b.parse_args()
    Створення_запис(аргументи.шлях)
