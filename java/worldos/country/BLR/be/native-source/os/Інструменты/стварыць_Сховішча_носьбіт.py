#!/usr/bin/env python3
"""새 파일에만 JKSTORE1 전용 сховішча_значэнне 매체를 만든다. 기존 Файл/장치는 덮어쓰지 않는다."""
import argparse
from pathlib import Path
import struct

def стварыць_увядзенне(ШЛЯХ):
    with Path(ШЛЯХ).open('xb') as Выхад:
        머리 = bytearray(512)
        struct.pack_into('<8sII', 머리, 0, b'JKSTORE1', 2048, 0x3153464a)
        Выхад.write(머리)
        Выхад.truncate(2048 * 512)

if __name__ == '__main__':
    аналізатар_48ee4b1b = argparse.ArgumentParser(description=__doc__)
    аналізатар_48ee4b1b.add_argument('ШЛЯХ')
    인수 = аналізатар_48ee4b1b.parse_args()
    стварыць_увядзенне(인수.ШЛЯХ)
