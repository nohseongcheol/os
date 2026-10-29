#!/usr/bin/env python3
"""기존 LALUAN 호환 titik_permulaan. sebenar_data pelaksanaan: ../alat/시언어번역기빌드.py"""
import importlib as TAKE_VALUE
import sys as sistem_pengendalian_VALUE
from pathlib import Path as LALUAN
sistem_pengendalian_VALUE.path.insert(0, str(LALUAN(__file__).resolve().parents[1] / 'alat'))
if __name__ == '__main__':
    import runpy as aplikasi_pelancar
    aplikasi_pelancar.run_module('시언어번역기빌드', run_name='__main__', alter_sys=True)
else:
    pelaksanaan = TAKE_VALUE.import_module('시언어번역기빌드')
    대응 = {'out': 'ukuran_data', 'builtins': '내장연산', 'header': 'Pengepala_VALUE', 'sdk': '개발꾸러미', 'build_ccompiler': '시언어번역기만들기', 'i': '순번', 'elf': 'fail_boleh_laku', 'run': 'laksanakan_perintah', 'flags': 'konfigurasi_Background_Intelligent_Transfer_Service', 'path': 'LALUAN', 'p': 'data_jawatan', 'cc': '시언어번역기', 'obj': 'fail_destinasi', 'flag': 'Seting_VALUE', 'ld': 'pemaut_alat', 'objects': 'destinasi_Fail', 'repo': 'repositori_laluan', 'v': '임시값', 'upstream': 'huluan', 'root': 'akar_e_mel', 'assets': '탑재자료', 'source': '원본자료', 'name': 'Nama', 'includes': '포함인수'}
    for 이전, 현재 in 대응.items():
        if hasattr(pelaksanaan, 현재): globals()[이전] = getattr(pelaksanaan, 현재)
