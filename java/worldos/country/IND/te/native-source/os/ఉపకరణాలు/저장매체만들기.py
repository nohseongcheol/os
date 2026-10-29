#!/usr/bin/env python3
"""새 파일에만 JKSTORE1 전용 నిల్వ_మూల్యం 매체를 만든다. 기존 దస్త్రం/장치는 덮어쓰지 않는다."""
import argparse
from pathlib import Path
import struct

def క్రియేట్_ప్రవేశం(పాత్):
    with Path(పాత్).open('xb') as అవుట్పుట్:
        머리 = bytearray(512)
        struct.pack_into('<8sII', 머리, 0, b'JKSTORE1', 2048, 0x3153464a)
        అవుట్పుట్.write(머리)
        అవుట్పుట్.truncate(2048 * 512)

if __name__ == '__main__':
    పార్సర్_48ee4b1b = argparse.ArgumentParser(description=__doc__)
    పార్సర్_48ee4b1b.add_argument('పాత్')
    인수 = పార్సర్_48ee4b1b.parse_args()
    క్రియేట్_ప్రవేశం(인수.పాత్)
