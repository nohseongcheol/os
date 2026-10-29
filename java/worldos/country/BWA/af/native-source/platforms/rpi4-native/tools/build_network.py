#!/usr/bin/env python3
"""기존 Pad 호환 inskrywing_p. werklik_data 구현: ../Nutsmiddels/bou_Netwerk.py"""
import importlib as TAKE_VALUE
import sys as bedryfstelsel_VALUE
from pathlib import Path as Pad
bedryfstelsel_VALUE.path.insert(0, str(Pad(__file__).resolve().parents[1] / 'Nutsmiddels'))
if __name__ == '__main__':
    import runpy as program_oopmaker
    program_oopmaker.run_module('bou_Netwerk', run_name='__main__', alter_sys=True)
else:
    구현 = TAKE_VALUE.import_module('bou_Netwerk')
    대응 = {'obj': 'bestemmingslêer', 'objects': 'bestemming_Lêers', 'library': 'biblioteek', 'output': '출력결과', 'port': '접속번호', 'root': 'wortel_adres', 'files': 'lêer_Lys', 'source': '원본자료', 'run': 'uitvoer_bevel', 'flags': 'konfigurasie_Agtergrond_intelligente_oordragdiens', 'path': 'Pad', 'build_network': 'Skep_Netwerk', 'cc': '시언어번역기', 'ar': 'Argief_nutsmiddel'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
