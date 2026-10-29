#!/usr/bin/env python3
"""기존 LLWYBR 호환 cofnod_p. go_iawn_data 구현: ../Offer/allgludo_SDK.py"""
import importlib as TAKE_VALUE
import sys as system_weithredu_VALUE
from pathlib import Path as LLWYBR
system_weithredu_VALUE.path.insert(0, str(LLWYBR(__file__).resolve().parents[1] / 'Offer'))
if __name__ == '__main__':
    import runpy as Rhaglen_lansiwr
    Rhaglen_lansiwr.run_module('allgludo_SDK', run_name='__main__', alter_sys=True)
else:
    구현 = TAKE_VALUE.import_module('allgludo_SDK')
    대응 = {'out': 'mesur_data', 'obj': 'ffeil_derbyn', 'relative': '상대경로', 'compiler_archive': '번역기꾸러미', 'sdk': '개발꾸러미', 'dist': '배포경로', 'archive': 'Archif', 'main': 'Gweithredu_2', 'posix': '포직스경로', 'files': 'ffeil_Rhestr', 'source': '원본자료', 'name': 'Enw', 'target': 'targed', 'ROOT': 'prosiect_gwraidd', 'destination': 'cyrchfan_data_ADDRESS', 'manifest': '꾸러미명세', 'work': '작업경로'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
