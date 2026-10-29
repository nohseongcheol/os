#!/usr/bin/env python3
"""새 파일에만 JKSTORE1 전용 ablegenDatenWert 매체를 만든다. 기존 Datei/장치는 덮어쓰지 않는다."""
import argparse
from pathlib import Path
import struct

def eintragErstellen(pfad):
    with Path(pfad).open('xb') as Ausgabe:
        kopfWert = bytearray(512)
        struct.pack_into('<8sII', kopfWert, 0, b'JKSTORE1', 2048, 0x3153464a)
        Ausgabe.write(kopfWert)
        Ausgabe.truncate(2048 * 512)

if __name__ == '__main__':
    Strukturanalysierer = argparse.ArgumentParser(description=__doc__)
    Strukturanalysierer.add_argument('pfad')
    argumente = Strukturanalysierer.parse_args()
    eintragErstellen(argumente.pfad)
