#!/usr/bin/env python3
"""기존 LLWYBR 호환 cofnod_p. go_iawn_data 구현: ../Offer/코딩시험.py"""
import importlib as TAKE_VALUE
import sys as system_weithredu_VALUE
from pathlib import Path as LLWYBR
system_weithredu_VALUE.path.insert(0, str(LLWYBR(__file__).resolve().parents[1] / 'Offer'))
if __name__ == '__main__':
    import runpy as Rhaglen_lansiwr
    Rhaglen_lansiwr.run_module('코딩시험', run_name='__main__', alter_sys=True)
else:
    구현 = TAKE_VALUE.import_module('코딩시험')
    대응 = {'out': 'mesur_data', 'expected': '예상결과', 'sdk': '개발꾸러미', 'suffix': '뒷부분', 'arc': '압축묶음', 'main': 'Gweithredu_2', 'elf': '실행파일', 'run': 'Gweithredu_gorchymyn', 'name': 'Enw', 'path': 'LLWYBR', 'p': 'data_safle', 'ROOT': 'prosiect_gwraidd', 'report': 'dilysu_adrodd', 'args': 'arg_ARAE'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
