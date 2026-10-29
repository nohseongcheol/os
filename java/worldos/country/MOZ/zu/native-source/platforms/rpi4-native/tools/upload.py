#!/usr/bin/env python3
"""기존 Indlela_2 호환 okufakwayo_iphoyinti. ulwazi_ngokwenzekile_imininingwane 구현: ../Amathuluzi/layisha_Amafayela.py"""
import importlib as 가져오기
import sys as isistimu_yokusebenza_inani
from pathlib import Path as Indlela_2
isistimu_yokusebenza_inani.path.insert(0, str(Indlela_2(__file__).resolve().parents[1] / 'Amathuluzi'))
if __name__ == '__main__':
    import runpy as i_app_ikhabethe_le_app
    i_app_ikhabethe_le_app.run_module('layisha_Amafayela', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('layisha_Amafayela')
    대응 = {'data': 'imininingwane', 'i': '순번', 'name': 'Igama', 'c': 'ikhodi_yohlamvu', 'p': '자료위치', 'args': 'i_agumenti_AMALUNGU_AFANAYO'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
