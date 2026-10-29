#!/usr/bin/env python3
"""기존 SLÓÐ 호환 færsla_P. raun_gögn 구현: ../Verkfæri/hlaða_upp_Skrár.py"""
import importlib as TAKE_VALUE
import sys as stýrikerfi_VALUE
from pathlib import Path as SLÓÐ
stýrikerfi_VALUE.path.insert(0, str(SLÓÐ(__file__).resolve().parents[1] / 'Verkfæri'))
if __name__ == '__main__':
    import runpy as forrit_ræsir
    forrit_ræsir.run_module('hlaða_upp_Skrár', run_name='__main__', alter_sys=True)
else:
    구현 = TAKE_VALUE.import_module('hlaða_upp_Skrár')
    vörpun_VALUE = {'data': 'gögn', 'i': '순번', 'name': 'Heiti', 'c': 'stafkóði', 'p': 'gögn_staða', 'args': 'frumbreyta_ARRAY'}
    for 이전, 현재 in vörpun_VALUE.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
