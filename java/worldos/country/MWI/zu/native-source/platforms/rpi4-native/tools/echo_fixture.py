#!/usr/bin/env python3
"""기존 Indlela_2 호환 okufakwayo_iphoyinti. ulwazi_ngokwenzekile_imininingwane 구현: ../Amathuluzi/되돌림시험서버.py"""
import importlib as 가져오기
import sys as isistimu_yokusebenza_inani
from pathlib import Path as Indlela_2
isistimu_yokusebenza_inani.path.insert(0, str(Indlela_2(__file__).resolve().parents[1] / 'Amathuluzi'))
if __name__ == '__main__':
    import runpy as i_app_ikhabethe_le_app
    i_app_ikhabethe_le_app.run_module('되돌림시험서버', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('되돌림시험서버')
    대응 = {'data': 'imininingwane', 'e': '보조항목', 'connection': 'uxhumano_e05f319b', 'f': 'ifayela_okufakwayo', 'peer': 'untanga_inani', 'self': '자신', 'udp': '전문제어', 't': '터미널항목', 'tcp': 'uxhumano_isilawuli', 'EchoFixture': '되돌림시험서버', 'args': 'i_agumenti_AMALUNGU_AFANAYO', 'chunk': '조각'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
