#!/usr/bin/env python3
"""기존 SLÓÐ 호환 færsla_P. raun_gögn 구현: ../Verkfæri/되돌림시험서버.py"""
import importlib as TAKE_VALUE
import sys as stýrikerfi_VALUE
from pathlib import Path as SLÓÐ
stýrikerfi_VALUE.path.insert(0, str(SLÓÐ(__file__).resolve().parents[1] / 'Verkfæri'))
if __name__ == '__main__':
    import runpy as forrit_ræsir
    forrit_ræsir.run_module('되돌림시험서버', run_name='__main__', alter_sys=True)
else:
    구현 = TAKE_VALUE.import_module('되돌림시험서버')
    vörpun_VALUE = {'data': 'gögn', 'e': '보조항목', 'connection': 'tenging_e05f319b', 'f': 'skrá_færsla_3d0c1245', 'peer': 'jafningi_VALUE', 'self': '자신', 'udp': '전문제어', 't': 'Endastöð_færsla', 'tcp': 'tenging_stýring', 'EchoFixture': '되돌림시험서버', 'args': 'frumbreyta_ARRAY', 'chunk': '조각'}
    for 이전, 현재 in vörpun_VALUE.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
