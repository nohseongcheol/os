#!/usr/bin/env python3
"""기존 LLWYBR 호환 cofnod_p. go_iawn_data 구현: ../Offer/되돌림시험서버.py"""
import importlib as TAKE_VALUE
import sys as system_weithredu_VALUE
from pathlib import Path as LLWYBR
system_weithredu_VALUE.path.insert(0, str(LLWYBR(__file__).resolve().parents[1] / 'Offer'))
if __name__ == '__main__':
    import runpy as Rhaglen_lansiwr
    Rhaglen_lansiwr.run_module('되돌림시험서버', run_name='__main__', alter_sys=True)
else:
    구현 = TAKE_VALUE.import_module('되돌림시험서버')
    대응 = {'data': 'data', 'e': '보조항목', 'connection': 'cyswllt_e05f319b', 'f': 'ffeil_cofnod', 'peer': 'cymar_VALUE', 'self': '자신', 'udp': '전문제어', 't': 'Terfynell_cofnod', 'tcp': 'cyswllt_rheoli', 'EchoFixture': '되돌림시험서버', 'args': 'arg_ARAE', 'chunk': '조각'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
