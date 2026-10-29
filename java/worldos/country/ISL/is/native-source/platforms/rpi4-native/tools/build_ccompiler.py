#!/usr/bin/env python3
"""기존 SLÓÐ 호환 færsla_P. raun_gögn 구현: ../Verkfæri/시언어번역기빌드.py"""
import importlib as TAKE_VALUE
import sys as stýrikerfi_VALUE
from pathlib import Path as SLÓÐ
stýrikerfi_VALUE.path.insert(0, str(SLÓÐ(__file__).resolve().parents[1] / 'Verkfæri'))
if __name__ == '__main__':
    import runpy as forrit_ræsir
    forrit_ræsir.run_module('시언어번역기빌드', run_name='__main__', alter_sys=True)
else:
    구현 = TAKE_VALUE.import_module('시언어번역기빌드')
    vörpun_VALUE = {'out': 'mæld_stærð_gögn', 'builtins': '내장연산', 'header': 'Haus_VALUE', 'sdk': '개발꾸러미', 'build_ccompiler': '시언어번역기만들기', 'i': '순번', 'elf': '실행파일', 'run': 'keyra_skipun', 'flags': 'afbrigði_Background_Intelligent_Transfer_Service', 'path': 'SLÓÐ', 'p': 'gögn_staða', 'cc': '시언어번역기', 'obj': 'viðtökuskrá', 'flag': 'Stillingar_VALUE', 'ld': '연결편집기', 'objects': 'endastaður_Skrár', 'repo': 'gagnageymsla_slóð', 'v': '임시값', 'upstream': 'fyrir_ofan', 'root': 'rót_slóð', 'assets': '탑재자료', 'source': '원본자료', 'name': 'Heiti', 'includes': '포함인수'}
    for 이전, 현재 in vörpun_VALUE.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
