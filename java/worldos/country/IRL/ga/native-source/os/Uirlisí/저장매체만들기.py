#!/usr/bin/env python3
"""새 파일에만 JKSTORE1 전용 Store_VALUE 매체를 만든다. 기존 Comhad/장치는 덮어쓰지 않는다."""
import argparse
from pathlib import Path
import struct

def Create_iontráil(CONAIR):
    with Path(CONAIR).open('xb') as Aschur:
        머리 = bytearray(512)
        struct.pack_into('<8sII', 머리, 0, b'JKSTORE1', 2048, 0x3153464a)
        Aschur.write(머리)
        Aschur.truncate(2048 * 512)

if __name__ == '__main__':
    해석기 = argparse.ArgumentParser(description=__doc__)
    해석기.add_argument('CONAIR')
    Argóintí = 해석기.parse_args()
    Create_iontráil(Argóintí.CONAIR)
