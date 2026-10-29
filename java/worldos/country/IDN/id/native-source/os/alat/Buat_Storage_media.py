#!/usr/bin/env python3
"""새 파일에만 JKSTORE1 전용 Store_VALUE 매체를 만든다. 기존 berkas/장치는 덮어쓰지 않는다."""
import argparse
from pathlib import Path
import struct

def Buat_entri(jalur):
    with Path(jalur).open('xb') as keluaranTeks:
        kepala_VALUE = bytearray(512)
        struct.pack_into('<8sII', kepala_VALUE, 0, b'JKSTORE1', 2048, 0x3153464a)
        keluaranTeks.write(kepala_VALUE)
        keluaranTeks.truncate(2048 * 512)

if __name__ == '__main__':
    parser_48ee4b1b = argparse.ArgumentParser(description=__doc__)
    parser_48ee4b1b.add_argument('jalur')
    argumen = parser_48ee4b1b.parse_args()
    Buat_entri(argumen.jalur)
