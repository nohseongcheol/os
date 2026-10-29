#!/usr/bin/env python3
"""새 파일에만 JKSTORE1 전용 ସଞ୍ଚୟ_କରିବା_ମୂଲ୍ୟ 매체를 만든다. 기존 ଫାଇଲ/장치는 덮어쓰지 않는다."""
import argparse
from pathlib import Path
import struct

def ସୃଷ୍ଟି_ଏଣ୍ଟ୍ରି(ପଥ):
    with Path(ପଥ).open('xb') as ନିର୍ଗମ:
        머리 = bytearray(512)
        struct.pack_into('<8sII', 머리, 0, b'JKSTORE1', 2048, 0x3153464a)
        ନିର୍ଗମ.write(머리)
        ନିର୍ଗମ.truncate(2048 * 512)

if __name__ == '__main__':
    해석기 = argparse.ArgumentParser(description=__doc__)
    해석기.add_argument('ପଥ')
    인수 = 해석기.parse_args()
    ସୃଷ୍ଟି_ଏଣ୍ଟ୍ରି(인수.ପଥ)
