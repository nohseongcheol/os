#!/usr/bin/env python3
"""새 파일에만 JKSTORE1 전용 ذخیره_مقدار 매체를 만든다. 기존 پرونده/장치는 덮어쓰지 않는다."""
import argparse
from pathlib import Path
import struct

def ایجاد_ورودی(مسیر):
    with Path(مسیر).open('xb') as خروجی:
        머리 = bytearray(512)
        struct.pack_into('<8sII', 머리, 0, b'JKSTORE1', 2048, 0x3153464a)
        خروجی.write(머리)
        خروجی.truncate(2048 * 512)

if __name__ == '__main__':
    مفسر_48ee4b1b = argparse.ArgumentParser(description=__doc__)
    مفسر_48ee4b1b.add_argument('مسیر')
    نشانوندها = مفسر_48ee4b1b.parse_args()
    ایجاد_ورودی(نشانوندها.مسیر)
