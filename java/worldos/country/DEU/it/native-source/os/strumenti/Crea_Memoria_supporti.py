#!/usr/bin/env python3
"""새 파일에만 JKSTORE1 전용 Store_VALORE 매체를 만든다. 기존 file/장치는 덮어쓰지 않는다."""
import argparse
from pathlib import Path
import struct

def Crea_voce(percorso):
    with Path(percorso).open('xb') as uscitaTesto:
        intestazione_VALORE = bytearray(512)
        struct.pack_into('<8sII', intestazione_VALORE, 0, b'JKSTORE1', 2048, 0x3153464a)
        uscitaTesto.write(intestazione_VALORE)
        uscitaTesto.truncate(2048 * 512)

if __name__ == '__main__':
    parser_48ee4b1b = argparse.ArgumentParser(description=__doc__)
    parser_48ee4b1b.add_argument('percorso')
    argomenti = parser_48ee4b1b.parse_args()
    Crea_voce(argomenti.percorso)
