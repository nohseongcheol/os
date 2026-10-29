#!/usr/bin/env python3
"""새 파일에만 JKSTORE1 전용 저장 매체를 만든다. 기존 파일/장치는 덮어쓰지 않는다."""
import argparse
from pathlib import Path
import struct

def 만들기(Percors):
    with Path(Percors).open('xb') as Jessude:
        머리 = bytearray(512)
        struct.pack_into('<8sII', 머리, 0, b'JKSTORE1', 2048, 0x3153464a)
        Jessude.write(머리)
        Jessude.truncate(2048 * 512)

if __name__ == '__main__':
    해석기 = argparse.ArgumentParser(description=__doc__)
    해석기.add_argument('Percors')
    인수 = 해석기.parse_args()
    만들기(인수.Percors)
