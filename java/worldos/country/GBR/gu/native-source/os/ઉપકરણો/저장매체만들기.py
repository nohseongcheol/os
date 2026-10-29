#!/usr/bin/env python3
"""새 파일에만 JKSTORE1 전용 સંગ્રહ_કરવો_મૂલ્ય 매체를 만든다. 기존 ફાઈલ/장치는 덮어쓰지 않는다."""
import argparse
from pathlib import Path
import struct

def બનાવો_પ્રવેશ(પથ):
    with Path(પથ).open('xb') as આઉટપુટ:
        머리 = bytearray(512)
        struct.pack_into('<8sII', 머리, 0, b'JKSTORE1', 2048, 0x3153464a)
        આઉટપુટ.write(머리)
        આઉટપુટ.truncate(2048 * 512)

if __name__ == '__main__':
    해석기 = argparse.ArgumentParser(description=__doc__)
    해석기.add_argument('પથ')
    દલીલો = 해석기.parse_args()
    બનાવો_પ્રવેશ(દલીલો.પથ)
