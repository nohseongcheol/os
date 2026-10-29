#!/usr/bin/env python3
"""새 파일에만 JKSTORE1 전용 ساقلىماق_قىممىتى 매체를 만든다. 기존 ھۆججەت/장치는 덮어쓰지 않는다."""
import argparse
from pathlib import Path
import struct

def قۇرۇش_كىرگۈزۈش(يول):
    with Path(يول).open('xb') as چىقار:
        머리 = bytearray(512)
        struct.pack_into('<8sII', 머리, 0, b'JKSTORE1', 2048, 0x3153464a)
        چىقار.write(머리)
        چىقار.truncate(2048 * 512)

if __name__ == '__main__':
    해석기 = argparse.ArgumentParser(description=__doc__)
    해석기.add_argument('يول')
    ئۆزگەرگۈچىلەر = 해석기.parse_args()
    قۇرۇش_كىرگۈزۈش(ئۆزگەرگۈچىلەر.يول)
