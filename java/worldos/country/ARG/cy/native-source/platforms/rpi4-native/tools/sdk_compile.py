#!/usr/bin/env python3
"""기존 LLWYBR 호환 cofnod_p. go_iawn_data 구현: ../Offer/SDK_llunio.py"""
import importlib as TAKE_VALUE
import sys as system_weithredu_VALUE
from pathlib import Path as LLWYBR
system_weithredu_VALUE.path.insert(0, str(LLWYBR(__file__).resolve().parents[1] / 'Offer'))
if __name__ == '__main__':
    import runpy as Rhaglen_lansiwr
    Rhaglen_lansiwr.run_module('SDK_llunio', run_name='__main__', alter_sys=True)
else:
    구현 = TAKE_VALUE.import_module('SDK_llunio')
    대응 = {'compiler': '번역기', 'obj': 'ffeil_derbyn', 'sdk': '개발꾸러미', 'output': '출력결과', 'main': 'Gweithredu_2', 'elf': '실행파일', 'is_c': '시언어여부', 'parser': '인수해석기', 'language': 'Iaith', 'work': '작업경로', 'args': 'arg_ARAE'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
