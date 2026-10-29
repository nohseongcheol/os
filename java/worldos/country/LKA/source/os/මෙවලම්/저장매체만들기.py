#!/usr/bin/env python3
"""새 파일에만 JKSTORE1 전용 ගබඩා_කරන්න_අගය 매체를 만든다. 기존 ගොනු/장치는 덮어쓰지 않는다."""
import argparse
from pathlib import Path
import struct

def සාදන්න_පිවිසුම(මාර්_ගය):
    with Path(මාර්_ගය).open('xb') as 출력:
        머리 = bytearray(512)
        struct.pack_into('<8sII', 머리, 0, b'JKSTORE1', 2048, 0x3153464a)
        출력.write(머리)
        출력.truncate(2048 * 512)

if __name__ == '__main__':
    해석기 = argparse.ArgumentParser(description=__doc__)
    해석기.add_argument('මාර්_ගය')
    විස්තාරක = 해석기.parse_args()
    සාදන්න_පිවිසුම(විස්තාරක.මාර්_ගය)
