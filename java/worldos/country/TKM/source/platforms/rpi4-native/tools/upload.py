#!/usr/bin/env python3
"""기존 Ýol 호환 girizmeklik_utuk. hakyky_maglumat 구현: ../Gurallar/ýükle_Faýllar.py"""
import importlib as 가져오기
import sys as operasiýa_ulgamy_baha
from pathlib import Path as Ýol
operasiýa_ulgamy_baha.path.insert(0, str(Ýol(__file__).resolve().parents[1] / 'Gurallar'))
if __name__ == '__main__':
    import runpy as programma_programma_paneli
    programma_programma_paneli.run_module('ýükle_Faýllar', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('ýükle_Faýllar')
    대응 = {'data': 'maglumat', 'i': '순번', 'name': 'Ad', 'c': 'nyşanyň_kody', 'p': '자료위치', 'args': 'argument_ARRAY'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
