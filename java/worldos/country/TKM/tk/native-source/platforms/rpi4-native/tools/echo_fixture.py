#!/usr/bin/env python3
"""기존 Ýol 호환 girizmeklik_utuk. hakyky_maglumat 구현: ../Gurallar/되돌림시험서버.py"""
import importlib as 가져오기
import sys as operasiýa_ulgamy_baha
from pathlib import Path as Ýol
operasiýa_ulgamy_baha.path.insert(0, str(Ýol(__file__).resolve().parents[1] / 'Gurallar'))
if __name__ == '__main__':
    import runpy as programma_programma_paneli
    programma_programma_paneli.run_module('되돌림시험서버', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('되돌림시험서버')
    대응 = {'data': 'maglumat', 'e': '보조항목', 'connection': 'birikme_e05f319b', 'f': 'faýl_girizmeklik', 'peer': 'deň_derejeli_düwün_baha', 'self': '자신', 'udp': '전문제어', 't': '터미널항목', 'tcp': 'birikme_dolandyryş', 'EchoFixture': '되돌림시험서버', 'args': 'argument_ARRAY', 'chunk': '조각'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
