#!/usr/bin/env python3
"""기존 SLÓÐ 호환 færsla_P. raun_gögn 구현: ../Verkfæri/keyra_skipun.py"""
import importlib as TAKE_VALUE
import sys as stýrikerfi_VALUE
from pathlib import Path as SLÓÐ
stýrikerfi_VALUE.path.insert(0, str(SLÓÐ(__file__).resolve().parents[1] / 'Verkfæri'))
if __name__ == '__main__':
    import runpy as forrit_ræsir
    forrit_ræsir.run_module('keyra_skipun', run_name='__main__', alter_sys=True)
else:
    구현 = TAKE_VALUE.import_module('keyra_skipun')
    vörpun_VALUE = {'supported': '지원목록', 'parser': 'þáttari', 'qemu': '모의기계', 'run_desktop': 'runa_skjáborð', 'main': 'Keyra_2', 'host': 'hýsa', 'status': 'staða_VALUE_e10195a1', 'NetworkBridge': 'Net_brú', 'ROOT': 'verk_rót', 'bridge': 'brú', 'loader': '적재기', 'base': 'veggfóður_VALUE', 'options': 'valkostir', 'binary': 'tvíundar', 'args': 'frumbreyta_ARRAY', 'command': 'Skipun'}
    for 이전, 현재 in vörpun_VALUE.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
