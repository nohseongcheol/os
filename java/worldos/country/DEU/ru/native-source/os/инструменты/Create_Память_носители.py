#!/usr/bin/env python3
"""새 파일에만 JKSTORE1 전용 Store_ЗНАЧЕН 매체를 만든다. 기존 файл/장치는 덮어쓰지 않는다."""
import argparse
from pathlib import Path
import struct

def Create_ввод(путь):
    with Path(путь).open('xb') as текстовыйВывод:
        HEAD_ЗНАЧЕН = bytearray(512)
        struct.pack_into('<8sII', HEAD_ЗНАЧЕН, 0, b'JKSTORE1', 2048, 0x3153464a)
        текстовыйВывод.write(HEAD_ЗНАЧЕН)
        текстовыйВывод.truncate(2048 * 512)

if __name__ == '__main__':
    анализатор_48ee4b1b = argparse.ArgumentParser(description=__doc__)
    анализатор_48ee4b1b.add_argument('путь')
    аргументы = анализатор_48ee4b1b.parse_args()
    Create_ввод(аргументы.путь)
