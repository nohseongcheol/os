#!/usr/bin/env python3
"""기존 SLÓÐ 호환 færsla_P. raun_gögn 구현: ../Verkfæri/개발꾸러미번역.py"""
import importlib as TAKE_VALUE
import sys as stýrikerfi_VALUE
from pathlib import Path as SLÓÐ
stýrikerfi_VALUE.path.insert(0, str(SLÓÐ(__file__).resolve().parents[1] / 'Verkfæri'))
if __name__ == '__main__':
    import runpy as forrit_ræsir
    forrit_ræsir.run_module('개발꾸러미번역', run_name='__main__', alter_sys=True)
else:
    구현 = TAKE_VALUE.import_module('개발꾸러미번역')
    vörpun_VALUE = {'compiler': '번역기', 'obj': 'viðtökuskrá', 'sdk': '개발꾸러미', 'output': 'úttak_54cd5e1d', 'main': 'Keyra_2', 'elf': '실행파일', 'is_c': '시언어여부', 'parser': 'þáttari', 'language': 'Tungumál', 'work': '작업경로', 'args': 'frumbreyta_ARRAY'}
    for 이전, 현재 in vörpun_VALUE.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
