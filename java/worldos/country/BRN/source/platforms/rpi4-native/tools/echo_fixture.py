#!/usr/bin/env python3
"""기존 LALUAN 호환 titik_permulaan. sebenar_data pelaksanaan: ../alat/되돌림시험서버.py"""
import importlib as TAKE_VALUE
import sys as sistem_pengendalian_VALUE
from pathlib import Path as LALUAN
sistem_pengendalian_VALUE.path.insert(0, str(LALUAN(__file__).resolve().parents[1] / 'alat'))
if __name__ == '__main__':
    import runpy as aplikasi_pelancar
    aplikasi_pelancar.run_module('되돌림시험서버', run_name='__main__', alter_sys=True)
else:
    pelaksanaan = TAKE_VALUE.import_module('되돌림시험서버')
    대응 = {'data': 'data', 'e': '보조항목', 'connection': 'hubungan_e05f319b', 'f': 'fail_pemasukan', 'peer': 'rakan_VALUE', 'self': '자신', 'udp': '전문제어', 't': 'Terminal_pemasukan', 'tcp': 'hubungan_kawalan', 'EchoFixture': '되돌림시험서버', 'args': 'argumen_ARRAY', 'chunk': '조각'}
    for 이전, 현재 in 대응.items():
        if hasattr(pelaksanaan, 현재): globals()[이전] = getattr(pelaksanaan, 현재)
