#!/usr/bin/env python3
"""새 파일에만 JKSTORE1 전용 Store_نرخ 매체를 만든다. 기존 فایل/장치는 덮어쓰지 않는다."""
import argparse
from pathlib import Path
import struct

def دروستکردن_تێنووسین(گوزەر):
    with Path(گوزەر).open('xb') as 출력:
        머리 = bytearray(512)
        struct.pack_into('<8sII', 머리, 0, b'JKSTORE1', 2048, 0x3153464a)
        출력.write(머리)
        출력.truncate(2048 * 512)

if __name__ == '__main__':
    해석기 = argparse.ArgumentParser(description=__doc__)
    해석기.add_argument('گوزەر')
    인수 = 해석기.parse_args()
    دروستکردن_تێنووسین(인수.گوزەر)
