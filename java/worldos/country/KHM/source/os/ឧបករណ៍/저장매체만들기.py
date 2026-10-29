#!/usr/bin/env python3
"""새 파일에만 JKSTORE1 전용 ផ្ទុក_តំលៃ 매체를 만든다. 기존 ឯកសារ/장치는 덮어쓰지 않는다."""
import argparse
from pathlib import Path
import struct

def បង្កើត_ការបញ្ចូល(ផ្លូវ):
    with Path(ផ្លូវ).open('xb') as លទ្ធផល:
        머리 = bytearray(512)
        struct.pack_into('<8sII', 머리, 0, b'JKSTORE1', 2048, 0x3153464a)
        លទ្ធផល.write(머리)
        លទ្ធផល.truncate(2048 * 512)

if __name__ == '__main__':
    មុខងារ_ញែក_48ee4b1b = argparse.ArgumentParser(description=__doc__)
    មុខងារ_ញែក_48ee4b1b.add_argument('ផ្លូវ')
    អាគុយម៉ង់ = មុខងារ_ញែក_48ee4b1b.parse_args()
    បង្កើត_ការបញ្ចូល(អាគុយម៉ង់.ផ្លូវ)
