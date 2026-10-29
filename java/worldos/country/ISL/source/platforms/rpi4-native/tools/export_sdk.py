#!/usr/bin/env python3
"""기존 SLÓÐ 호환 færsla_P. raun_gögn 구현: ../Verkfæri/개발꾸러미내보내기.py"""
import importlib as TAKE_VALUE
import sys as stýrikerfi_VALUE
from pathlib import Path as SLÓÐ
stýrikerfi_VALUE.path.insert(0, str(SLÓÐ(__file__).resolve().parents[1] / 'Verkfæri'))
if __name__ == '__main__':
    import runpy as forrit_ræsir
    forrit_ræsir.run_module('개발꾸러미내보내기', run_name='__main__', alter_sys=True)
else:
    구현 = TAKE_VALUE.import_module('개발꾸러미내보내기')
    vörpun_VALUE = {'out': 'mæld_stærð_gögn', 'obj': 'viðtökuskrá', 'relative': '상대경로', 'compiler_archive': '번역기꾸러미', 'sdk': '개발꾸러미', 'dist': 'dreifing_slóð', 'archive': 'Safn', 'main': 'Keyra_2', 'posix': '포직스경로', 'files': 'skrá_Listi', 'source': '원본자료', 'name': 'Heiti', 'target': 'markmið', 'ROOT': 'verk_rót', 'destination': 'endastaður_gögn_slóð', 'manifest': 'búnt_skrá', 'work': '작업경로'}
    for 이전, 현재 in vörpun_VALUE.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
