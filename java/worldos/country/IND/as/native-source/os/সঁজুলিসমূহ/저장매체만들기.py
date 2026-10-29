#!/usr/bin/env python3
"""새 파일에만 JKSTORE1 전용 জমা_কৰক_মান 매체를 만든다. 기존 নথিপত্ৰ/장치는 덮어쓰지 않는다."""
import argparse
from pathlib import Path
import struct

def ক্ৰিয়েট_প্রবিষ্ট(পথ):
    with Path(পথ).open('xb') as নিৰ্গম:
        머리 = bytearray(512)
        struct.pack_into('<8sII', 머리, 0, b'JKSTORE1', 2048, 0x3153464a)
        নিৰ্গম.write(머리)
        নিৰ্গম.truncate(2048 * 512)

if __name__ == '__main__':
    해석기 = argparse.ArgumentParser(description=__doc__)
    해석기.add_argument('পথ')
    인수 = 해석기.parse_args()
    ক্ৰিয়েট_প্রবিষ্ট(인수.পথ)
