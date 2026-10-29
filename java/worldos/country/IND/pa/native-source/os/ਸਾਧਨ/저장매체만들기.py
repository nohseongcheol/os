#!/usr/bin/env python3
"""새 파일에만 JKSTORE1 전용 ਸੰਭਾਲੋ_ਕੀਮਤ 매체를 만든다. 기존 ਫਾਇਲ/장치는 덮어쓰지 않는다."""
import argparse
from pathlib import Path
import struct

def ਬਣਾਓ_ਦਾਖਲਾ(ਮਾਰਗ):
    with Path(ਮਾਰਗ).open('xb') as ਆਉਟਪੁੱਟ:
        머리 = bytearray(512)
        struct.pack_into('<8sII', 머리, 0, b'JKSTORE1', 2048, 0x3153464a)
        ਆਉਟਪੁੱਟ.write(머리)
        ਆਉਟਪੁੱਟ.truncate(2048 * 512)

if __name__ == '__main__':
    해석기 = argparse.ArgumentParser(description=__doc__)
    해석기.add_argument('ਮਾਰਗ')
    ਆਰਗੂਮੈਂਟ = 해석기.parse_args()
    ਬਣਾਓ_ਦਾਖਲਾ(ਆਰਗੂਮੈਂਟ.ਮਾਰਗ)
