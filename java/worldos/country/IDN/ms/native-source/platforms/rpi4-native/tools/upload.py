#!/usr/bin/env python3
"""기존 LALUAN 호환 titik_permulaan. sebenar_data pelaksanaan: ../alat/Upload_Fail.py"""
import importlib as TAKE_VALUE
import sys as sistem_pengendalian_VALUE
from pathlib import Path as LALUAN
sistem_pengendalian_VALUE.path.insert(0, str(LALUAN(__file__).resolve().parents[1] / 'alat'))
if __name__ == '__main__':
    import runpy as aplikasi_pelancar
    aplikasi_pelancar.run_module('Upload_Fail', run_name='__main__', alter_sys=True)
else:
    pelaksanaan = TAKE_VALUE.import_module('Upload_Fail')
    대응 = {'data': 'data', 'i': '순번', 'name': 'Nama', 'c': 'titik_kod', 'p': 'data_jawatan', 'args': 'argumen_ARRAY'}
    for 이전, 현재 in 대응.items():
        if hasattr(pelaksanaan, 현재): globals()[이전] = getattr(pelaksanaan, 현재)
