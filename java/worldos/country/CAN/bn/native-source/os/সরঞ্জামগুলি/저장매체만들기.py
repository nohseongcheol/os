#!/usr/bin/env python3
"""새 파일에만 JKSTORE1 전용 ভাণ্ডার_মান 매체를 만든다. 기존 নথির_নাম/장치는 덮어쓰지 않는다."""
import argparse
from pathlib import Path
import struct

def ক্রিয়েট_ভুক্তি(পথ_2):
    with Path(পথ_2).open('xb') as নির্গম:
        머리 = bytearray(512)
        struct.pack_into('<8sII', 머리, 0, b'JKSTORE1', 2048, 0x3153464a)
        নির্গম.write(머리)
        নির্গম.truncate(2048 * 512)

if __name__ == '__main__':
    পার্সার_48ee4b1b = argparse.ArgumentParser(description=__doc__)
    পার্সার_48ee4b1b.add_argument('পথ_2')
    আর্গুমেন্ট_তালিকা = পার্সার_48ee4b1b.parse_args()
    ক্রিয়েট_ভুক্তি(আর্গুমেন্ট_তালিকা.পথ_2)
