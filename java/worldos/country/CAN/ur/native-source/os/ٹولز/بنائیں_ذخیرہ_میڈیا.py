#!/usr/bin/env python3
"""새 파일에만 JKSTORE1 전용 ذخیرہ_کریں_قدر 매체를 만든다. 기존 فائل_کا_نام/장치는 덮어쓰지 않는다."""
import argparse
from pathlib import Path
import struct

def بنائیں_اندراج(راستہ_2):
    with Path(راستہ_2).open('xb') as اخراج_کا_مقام:
        머리 = bytearray(512)
        struct.pack_into('<8sII', 머리, 0, b'JKSTORE1', 2048, 0x3153464a)
        اخراج_کا_مقام.write(머리)
        اخراج_کا_مقام.truncate(2048 * 512)

if __name__ == '__main__':
    해석기 = argparse.ArgumentParser(description=__doc__)
    해석기.add_argument('راستہ_2')
    دلائل = 해석기.parse_args()
    بنائیں_اندراج(دلائل.راستہ_2)
