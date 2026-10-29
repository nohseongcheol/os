#!/usr/bin/env python3
"""기존 LALUAN 호환 titik_permulaan. sebenar_data pelaksanaan: ../alat/Eksport_SDK.py"""
import importlib as TAKE_VALUE
import sys as sistem_pengendalian_VALUE
from pathlib import Path as LALUAN
sistem_pengendalian_VALUE.path.insert(0, str(LALUAN(__file__).resolve().parents[1] / 'alat'))
if __name__ == '__main__':
    import runpy as aplikasi_pelancar
    aplikasi_pelancar.run_module('Eksport_SDK', run_name='__main__', alter_sys=True)
else:
    pelaksanaan = TAKE_VALUE.import_module('Eksport_SDK')
    대응 = {'out': 'ukuran_data', 'obj': 'fail_destinasi', 'relative': 'laluan_relatif', 'compiler_archive': '번역기꾸러미', 'sdk': '개발꾸러미', 'dist': '배포경로', 'archive': 'Arkib', 'main': 'Jalan', 'posix': '포직스경로', 'files': 'fail_Senarai', 'source': '원본자료', 'name': 'Nama', 'target': 'sasaran', 'ROOT': 'projek_akar', 'destination': 'destinasi_data_e_mel', 'manifest': 'pakej_manifes_aplikasi', 'work': '작업경로'}
    for 이전, 현재 in 대응.items():
        if hasattr(pelaksanaan, 현재): globals()[이전] = getattr(pelaksanaan, 현재)
