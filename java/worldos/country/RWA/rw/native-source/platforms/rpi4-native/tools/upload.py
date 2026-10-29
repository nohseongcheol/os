#!/usr/bin/env python3
"""기존 Inzira 호환 icyinjizwa_inota. nyakuri_amakurushingiro 구현: ../Ibikoresho/gukurura_Dosiye.py"""
import importlib as 가져오기
import sys as sisitemu_ngengamikorere_agaciro
from pathlib import Path as Inzira
sisitemu_ngengamikorere_agaciro.path.insert(0, str(Inzira(__file__).resolve().parents[1] / 'Ibikoresho'))
if __name__ == '__main__':
    import runpy as porogaramu_umukozi
    porogaramu_umukozi.run_module('gukurura_Dosiye', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('gukurura_Dosiye')
    대응 = {'data': 'amakurushingiro', 'i': '순번', 'name': 'Izina', 'c': '문자값', 'p': '자료위치', 'args': 'ingingo_ARRAY'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
