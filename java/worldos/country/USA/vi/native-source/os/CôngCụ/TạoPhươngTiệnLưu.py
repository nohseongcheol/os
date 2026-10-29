#!/usr/bin/env python3
"""새 파일에만 JKSTORE1 전용 giáTrịCất 매체를 만든다. 기존 Tệp/장치는 덮어쓰지 않는다."""
import argparse
from pathlib import Path
import struct

def tạoMục(đườngDẫn):
    with Path(đườngDẫn).open('xb') as ĐầuRa:
        giáTrịĐầu = bytearray(512)
        struct.pack_into('<8sII', giáTrịĐầu, 0, b'JKSTORE1', 2048, 0x3153464a)
        ĐầuRa.write(giáTrịĐầu)
        ĐầuRa.truncate(2048 * 512)

if __name__ == '__main__':
    BộPhânTích = argparse.ArgumentParser(description=__doc__)
    BộPhânTích.add_argument('đườngDẫn')
    cácĐốiSố = BộPhânTích.parse_args()
    tạoMục(cácĐốiSố.đườngDẫn)
