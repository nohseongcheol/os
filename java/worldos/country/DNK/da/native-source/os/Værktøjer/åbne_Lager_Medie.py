#!/usr/bin/env python3
"""새 파일에만 JKSTORE1 전용 Store_VÆRDI 매체를 만든다. 기존 Fil/장치는 덮어쓰지 않는다."""
import argparse
from pathlib import Path
import struct

def åbne_post_81b8d99b(Sti):
    with Path(Sti).open('xb') as Udgang:
        머리 = bytearray(512)
        struct.pack_into('<8sII', 머리, 0, b'JKSTORE1', 2048, 0x3153464a)
        Udgang.write(머리)
        Udgang.truncate(2048 * 512)

if __name__ == '__main__':
    parser_48ee4b1b = argparse.ArgumentParser(description=__doc__)
    parser_48ee4b1b.add_argument('Sti')
    Argumenter = parser_48ee4b1b.parse_args()
    åbne_post_81b8d99b(Argumenter.Sti)
