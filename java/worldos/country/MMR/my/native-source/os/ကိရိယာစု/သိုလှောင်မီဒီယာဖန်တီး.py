#!/usr/bin/env python3
"""새 파일에만 JKSTORE1 전용 သိုလှောင်တန်ဖိုး 매체를 만든다. 기존 ဖိုင်/장치는 덮어쓰지 않는다."""
import argparse
from pathlib import Path
import struct

def အချက်ဖန်တီး(လမ်း):
    with Path(လမ်း).open('xb') as အထွက်:
        ဦးခေါင်းတန်ဖိုး = bytearray(512)
        struct.pack_into('<8sII', ဦးခေါင်းတန်ဖိုး, 0, b'JKSTORE1', 2048, 0x3153464a)
        အထွက်.write(ဦးခေါင်းတန်ဖိုး)
        အထွက်.truncate(2048 * 512)

if __name__ == '__main__':
    해석기 = argparse.ArgumentParser(description=__doc__)
    해석기.add_argument('လမ်း')
    အချက်များ = 해석기.parse_args()
    အချက်ဖန်တီး(အချက်များ.လမ်း)
