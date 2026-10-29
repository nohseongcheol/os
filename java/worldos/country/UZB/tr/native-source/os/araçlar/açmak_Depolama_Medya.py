#!/usr/bin/env python3
"""새 파일에만 JKSTORE1 전용 depo_değer 매체를 만든다. 기존 dosya/장치는 덮어쓰지 않는다."""
import argparse
from pathlib import Path
import struct

def açmak_girdi(yol):
    with Path(yol).open('xb') as metinÇıktısı:
        머리 = bytearray(512)
        struct.pack_into('<8sII', 머리, 0, b'JKSTORE1', 2048, 0x3153464a)
        metinÇıktısı.write(머리)
        metinÇıktısı.truncate(2048 * 512)

if __name__ == '__main__':
    ayrıştırıcı_48ee4b1b = argparse.ArgumentParser(description=__doc__)
    ayrıştırıcı_48ee4b1b.add_argument('yol')
    bağımsız_değişkenler = ayrıştırıcı_48ee4b1b.parse_args()
    açmak_girdi(bağımsız_değişkenler.yol)
