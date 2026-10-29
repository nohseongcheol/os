#!/usr/bin/env python3
"""새 파일에만 JKSTORE1 전용 സ്_റ്റോർ_മൂല്യം 매체를 만든다. 기존 ഫയല്/장치는 덮어쓰지 않는다."""
import argparse
from pathlib import Path
import struct

def സൃഷ്_ടിക്കുക_എന്_ട്രി(വഴി):
    with Path(വഴി).open('xb') as ഫലം:
        머리 = bytearray(512)
        struct.pack_into('<8sII', 머리, 0, b'JKSTORE1', 2048, 0x3153464a)
        ഫലം.write(머리)
        ഫലം.truncate(2048 * 512)

if __name__ == '__main__':
    പാഴ്_സർ_48ee4b1b = argparse.ArgumentParser(description=__doc__)
    പാഴ്_സർ_48ee4b1b.add_argument('വഴി')
    인수 = പാഴ്_സർ_48ee4b1b.parse_args()
    സൃഷ്_ടിക്കുക_എന്_ട്രി(인수.വഴി)
