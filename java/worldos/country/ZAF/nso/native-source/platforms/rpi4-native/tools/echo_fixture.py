#!/usr/bin/env python3
"""기존 Tsejana 호환 go_tsenya_tshedimošo_ntlha. kgonthe_data 구현: ../Ditholosi/되돌림시험서버.py"""
import importlib as 가져오기
import sys as tshepedišotirišo_boleng
from pathlib import Path as Tsejana
tshepedišotirišo_boleng.path.insert(0, str(Tsejana(__file__).resolve().parents[1] / 'Ditholosi'))
if __name__ == '__main__':
    import runpy as tirišo_sethala_tirišo
    tirišo_sethala_tirišo.run_module('되돌림시험서버', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('되돌림시험서버')
    대응 = {'data': 'data', 'e': '보조항목', 'connection': 'kgokaganya_e05f319b', 'f': 'faele_go_tsenya_tshedimošo', 'peer': 'sedirišwa_sa_legoro_le_tee_boleng', 'self': '자신', 'udp': '전문제어', 't': '터미널항목', 'tcp': 'kgokaganya_taolo', 'EchoFixture': '되돌림시험서버', 'args': 'akumente_arei', 'chunk': '조각'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
