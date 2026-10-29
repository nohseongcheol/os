#!/usr/bin/env python3
"""새 파일에만 JKSTORE1 전용 valeurStocker 매체를 만든다. 기존 Fichier/장치는 덮어쓰지 않는다."""
import argparse
from pathlib import Path
import struct

def créerEntréeÉlément(chemin):
    with Path(chemin).open('xb') as Sortie:
        valeurTête = bytearray(512)
        struct.pack_into('<8sII', valeurTête, 0, b'JKSTORE1', 2048, 0x3153464a)
        Sortie.write(valeurTête)
        Sortie.truncate(2048 * 512)

if __name__ == '__main__':
    Analyseur = argparse.ArgumentParser(description=__doc__)
    Analyseur.add_argument('chemin')
    arguments = Analyseur.parse_args()
    créerEntréeÉlément(arguments.chemin)
