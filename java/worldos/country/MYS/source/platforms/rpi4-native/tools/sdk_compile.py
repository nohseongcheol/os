#!/usr/bin/env python3
"""기존 LALUAN 호환 titik_permulaan. sebenar_data pelaksanaan: ../alat/SDK_bina.py"""
import importlib as TAKE_VALUE
import sys as sistem_pengendalian_VALUE
from pathlib import Path as LALUAN
sistem_pengendalian_VALUE.path.insert(0, str(LALUAN(__file__).resolve().parents[1] / 'alat'))
if __name__ == '__main__':
    import runpy as aplikasi_pelancar
    aplikasi_pelancar.run_module('SDK_bina', run_name='__main__', alter_sys=True)
else:
    pelaksanaan = TAKE_VALUE.import_module('SDK_bina')
    대응 = {'compiler': '번역기', 'obj': 'fail_destinasi', 'sdk': '개발꾸러미', 'output': '출력결과', 'main': 'Jalan', 'elf': 'fail_boleh_laku', 'is_c': 'teknologi_maklumat_C_Bahasa', 'parser': 'penghurai', 'language': 'Bahasa', 'work': '작업경로', 'args': 'argumen_ARRAY'}
    for 이전, 현재 in 대응.items():
        if hasattr(pelaksanaan, 현재): globals()[이전] = getattr(pelaksanaan, 현재)
