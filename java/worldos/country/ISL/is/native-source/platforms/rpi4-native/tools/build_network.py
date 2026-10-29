#!/usr/bin/env python3
"""기존 SLÓÐ 호환 færsla_P. raun_gögn 구현: ../Verkfæri/smíð_Net.py"""
import importlib as TAKE_VALUE
import sys as stýrikerfi_VALUE
from pathlib import Path as SLÓÐ
stýrikerfi_VALUE.path.insert(0, str(SLÓÐ(__file__).resolve().parents[1] / 'Verkfæri'))
if __name__ == '__main__':
    import runpy as forrit_ræsir
    forrit_ræsir.run_module('smíð_Net', run_name='__main__', alter_sys=True)
else:
    구현 = TAKE_VALUE.import_module('smíð_Net')
    vörpun_VALUE = {'obj': 'viðtökuskrá', 'objects': 'endastaður_Skrár', 'library': 'safn', 'output': 'úttak_54cd5e1d', 'port': 'tengisnúmer', 'root': 'rót_slóð', 'files': 'skrá_Listi', 'source': '원본자료', 'run': 'keyra_skipun', 'flags': 'afbrigði_Background_Intelligent_Transfer_Service', 'path': 'SLÓÐ', 'build_network': 'stofna_Net', 'cc': '시언어번역기', 'ar': 'Safn_verkfæri'}
    for 이전, 현재 in vörpun_VALUE.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
