#!/usr/bin/env python3
"""새 파일에만 JKSTORE1 전용 Store_VALUE 매체를 만든다. 기존 Ffeil/장치는 덮어쓰지 않는다."""
import argparse
from pathlib import Path
import struct

def Creu_cofnod(LLWYBR):
    with Path(LLWYBR).open('xb') as Allbwn:
        머리 = bytearray(512)
        struct.pack_into('<8sII', 머리, 0, b'JKSTORE1', 2048, 0x3153464a)
        Allbwn.write(머리)
        Allbwn.truncate(2048 * 512)

if __name__ == '__main__':
    해석기 = argparse.ArgumentParser(description=__doc__)
    해석기.add_argument('LLWYBR')
    인수 = 해석기.parse_args()
    Creu_cofnod(인수.LLWYBR)
