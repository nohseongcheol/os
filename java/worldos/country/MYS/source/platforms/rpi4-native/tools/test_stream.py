#!/usr/bin/env python3
"""기존 LALUAN 호환 titik_permulaan. sebenar_data pelaksanaan: ../alat/ujian_strim.py"""
import importlib as TAKE_VALUE
import sys as sistem_pengendalian_VALUE
from pathlib import Path as LALUAN
sistem_pengendalian_VALUE.path.insert(0, str(LALUAN(__file__).resolve().parents[1] / 'alat'))
if __name__ == '__main__':
    import runpy as aplikasi_pelancar
    aplikasi_pelancar.run_module('ujian_strim', run_name='__main__', alter_sys=True)
else:
    pelaksanaan = TAKE_VALUE.import_module('ujian_strim')
    대응 = {'out': 'ukuran_data', 'main': 'Jalan', 'ROOT': 'projek_akar', 'p': 'data_jawatan', 'text': 'Teks', 'report': 'pensahihan_lapor'}
    for 이전, 현재 in 대응.items():
        if hasattr(pelaksanaan, 현재): globals()[이전] = getattr(pelaksanaan, 현재)
