#!/usr/bin/env python3
"""기존 SLÓÐ 호환 færsla_P. raun_gögn 구현: ../Verkfæri/자바가상기계시험.py"""
import importlib as TAKE_VALUE
import sys as stýrikerfi_VALUE
from pathlib import Path as SLÓÐ
stýrikerfi_VALUE.path.insert(0, str(SLÓÐ(__file__).resolve().parents[1] / 'Verkfæri'))
if __name__ == '__main__':
    import runpy as forrit_ræsir
    forrit_ræsir.run_module('자바가상기계시험', run_name='__main__', alter_sys=True)
else:
    구현 = TAKE_VALUE.import_module('자바가상기계시험')
    vörpun_VALUE = {'message': '알림문', 's': 'strengur_gögn', 'actual': 'raun_mæld_stærð', 'match': '일치', 'payload': 'farmur_gögn', 'cases': '시험사례', 'fixture': '시험자료', 'main': 'Keyra_2', 'ROOT': 'verk_rót', 'text': 'Texti', 'valid': '유효함', 'includes': '포함인수', 'include': '포함항목', 'expected': '예상결과', 'sources': '원문목록', 'tmp': '임시경로', 'done': 'lokið_upphæð', 'classes': 'klasi_slóð', 'output': 'úttak_54cd5e1d', 'result': 'NIÐURSTAÐA', 'cmd': '명령인수', 'name': 'Heiti', 'jar': '자바꾸러미', 'report': 'prófun_skrá', 'tests': '시험목록'}
    for 이전, 현재 in vörpun_VALUE.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
