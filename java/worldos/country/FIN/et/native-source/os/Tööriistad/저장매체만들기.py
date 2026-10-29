#!/usr/bin/env python3
"""새 파일에만 JKSTORE1 전용 salv_VALUE 매체를 만든다. 기존 Fail/장치는 덮어쓰지 않는다."""
import argparse
from pathlib import Path
import struct

def avama_kirje(RADA):
    with Path(RADA).open('xb') as Väljund:
        머리 = bytearray(512)
        struct.pack_into('<8sII', 머리, 0, b'JKSTORE1', 2048, 0x3153464a)
        Väljund.write(머리)
        Väljund.truncate(2048 * 512)

if __name__ == '__main__':
    parser_48ee4b1b = argparse.ArgumentParser(description=__doc__)
    parser_48ee4b1b.add_argument('RADA')
    Argumendid = parser_48ee4b1b.parse_args()
    avama_kirje(Argumendid.RADA)
