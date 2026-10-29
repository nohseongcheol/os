#!/usr/bin/env python3
"""기존 yo_l 호환 kiritish_nuqta. real_ma_lumotlar 구현: ../Vositalar/되돌림시험서버.py"""
import importlib as TAKE_VALUE
import sys as operatsion_tizim_VALUE
from pathlib import Path as yo_l
operatsion_tizim_VALUE.path.insert(0, str(yo_l(__file__).resolve().parents[1] / 'Vositalar'))
if __name__ == '__main__':
    import runpy as ilova_ilovalar_paneli
    ilova_ilovalar_paneli.run_module('되돌림시험서버', run_name='__main__', alter_sys=True)
else:
    구현 = TAKE_VALUE.import_module('되돌림시험서버')
    대응 = {'data': 'ma_lumotlar', 'e': '보조항목', 'connection': 'aloqa_e05f319b', 'f': 'fayl_kiritish', 'peer': 'bir_rangli_VALUE', 'self': '자신', 'udp': '전문제어', 't': 'Terminal_kiritish', 'tcp': 'aloqa_boshqaruv', 'EchoFixture': '되돌림시험서버', 'args': 'dalil_ARRAY', 'chunk': '조각'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
