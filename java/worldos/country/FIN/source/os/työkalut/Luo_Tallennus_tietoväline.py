#!/usr/bin/env python3
"""새 파일에만 JKSTORE1 전용 Store_ARVO 매체를 만든다. 기존 tiedoston_nimi/장치는 덮어쓰지 않는다."""
import argparse
from pathlib import Path
import struct

def Luo_merkintä(polku_2):
    with Path(polku_2).open('xb') as tulostuspaikka:
        머리 = bytearray(512)
        struct.pack_into('<8sII', 머리, 0, b'JKSTORE1', 2048, 0x3153464a)
        tulostuspaikka.write(머리)
        tulostuspaikka.truncate(2048 * 512)

if __name__ == '__main__':
    jäsennin_48ee4b1b = argparse.ArgumentParser(description=__doc__)
    jäsennin_48ee4b1b.add_argument('polku_2')
    argumentit = jäsennin_48ee4b1b.parse_args()
    Luo_merkintä(argumentit.polku_2)
