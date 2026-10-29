#!/usr/bin/env python3
"""기존 SLÓÐ 호환 færsla_P. raun_gögn 구현: ../Verkfæri/예제빌드.py"""
import importlib as TAKE_VALUE
import sys as stýrikerfi_VALUE
from pathlib import Path as SLÓÐ
stýrikerfi_VALUE.path.insert(0, str(SLÓÐ(__file__).resolve().parents[1] / 'Verkfæri'))
if __name__ == '__main__':
    import runpy as forrit_ræsir
    forrit_ræsir.run_module('예제빌드', run_name='__main__', alter_sys=True)
else:
    구현 = TAKE_VALUE.import_module('예제빌드')
    vörpun_VALUE = {'out': 'mæld_stærð_gögn', 'build_examples': '예제만들기', 'files': 'skrá_Listi', 'java': '자바실행', 'run': 'keyra_skipun', 'path': 'SLÓÐ', 'p': 'gögn_staða', 'readme': 'LESTUMIG', 'build_java_library': '자바라이브러리만들기', 'code': 'skipun_SEQUENCE', 'index': 'LOOKUP_INDEX', 'classes': 'klasi_slóð', 'repo': 'gagnageymsla_slóð', 'root': 'rót_slóð', 'content': 'Efni_VALUE', 'source': '원본자료', 'name': 'Heiti', 'target': 'markmið', 'manifest': 'búnt_skrá', 'language': 'Tungumál'}
    for 이전, 현재 in vörpun_VALUE.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
