#!/usr/bin/env python3
"""새 파일에만 JKSTORE1 전용 Ajiye_Daraja 매체를 만든다. 기존 Fayil/장치는 덮어쓰지 않는다."""
import argparse
from pathlib import Path
import struct

def ƙirƙíra_Mashigar_bayanai(Hanyar_shiga):
    with Path(Hanyar_shiga).open('xb') as 출력:
        머리 = bytearray(512)
        struct.pack_into('<8sII', 머리, 0, b'JKSTORE1', 2048, 0x3153464a)
        출력.write(머리)
        출력.truncate(2048 * 512)

if __name__ == '__main__':
    tatsar_manhaja_48ee4b1b = argparse.ArgumentParser(description=__doc__)
    tatsar_manhaja_48ee4b1b.add_argument('Hanyar_shiga')
    인수 = tatsar_manhaja_48ee4b1b.parse_args()
    ƙirƙíra_Mashigar_bayanai(인수.Hanyar_shiga)
