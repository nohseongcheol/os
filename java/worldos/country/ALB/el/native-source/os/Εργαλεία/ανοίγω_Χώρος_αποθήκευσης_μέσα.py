#!/usr/bin/env python3
"""새 파일에만 JKSTORE1 전용 αποθηκεύω_τιμή 매체를 만든다. 기존 Αρχείο/장치는 덮어쓰지 않는다."""
import argparse
from pathlib import Path
import struct

def ανοίγω_καταχώρηση(ΔΙΑΔΡΟΜΗ):
    with Path(ΔΙΑΔΡΟΜΗ).open('xb') as Έξοδος:
        머리 = bytearray(512)
        struct.pack_into('<8sII', 머리, 0, b'JKSTORE1', 2048, 0x3153464a)
        Έξοδος.write(머리)
        Έξοδος.truncate(2048 * 512)

if __name__ == '__main__':
    ανάλυση_48ee4b1b = argparse.ArgumentParser(description=__doc__)
    ανάλυση_48ee4b1b.add_argument('ΔΙΑΔΡΟΜΗ')
    Παράμετροι = ανάλυση_48ee4b1b.parse_args()
    ανοίγω_καταχώρηση(Παράμετροι.ΔΙΑΔΡΟΜΗ)
