#!/usr/bin/env python3
"""새 파일에만 JKSTORE1 전용 Store_VALUE 매체를 만든다. 기존 Failas/장치는 덮어쓰지 않는다."""
import argparse
from pathlib import Path
import struct

def kurti_įrašas(KELIAS):
    with Path(KELIAS).open('xb') as Išvestis:
        머리 = bytearray(512)
        struct.pack_into('<8sII', 머리, 0, b'JKSTORE1', 2048, 0x3153464a)
        Išvestis.write(머리)
        Išvestis.truncate(2048 * 512)

if __name__ == '__main__':
    analizatorius_48ee4b1b = argparse.ArgumentParser(description=__doc__)
    analizatorius_48ee4b1b.add_argument('KELIAS')
    Argumentai = analizatorius_48ee4b1b.parse_args()
    kurti_įrašas(Argumentai.KELIAS)
