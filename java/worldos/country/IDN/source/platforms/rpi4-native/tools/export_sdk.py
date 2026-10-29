#!/usr/bin/env python3
"""기존 jalur 호환 entri_p. aktual_data implementasi: ../alat/Ekspor_SDK.py"""
import importlib as TAKE_VALUE
import sys as sistem_operasi_VALUE
from pathlib import Path as jalur
sistem_operasi_VALUE.path.insert(0, str(jalur(__file__).resolve().parents[1] / 'alat'))
if __name__ == '__main__':
    import runpy as apl_peluncur
    apl_peluncur.run_module('Ekspor_SDK', run_name='__main__', alter_sys=True)
else:
    implementasi = TAKE_VALUE.import_module('Ekspor_SDK')
    대응 = {'out': 'KR_data', 'obj': 'file_tujuan', 'relative': '상대경로', 'compiler_archive': '번역기꾸러미', 'sdk': '개발꾸러미', 'dist': '배포경로', 'archive': 'Arsip', 'main': 'jalankan', 'posix': '포직스경로', 'files': 'file_Daftar', 'source': '원본자료', 'name': 'Nama_2', 'target': 'target', 'ROOT': 'Tugas_akar', 'destination': 'tujuan_data_surel', 'manifest': '꾸러미명세', 'work': '작업경로'}
    for 이전, saat_ini_item in 대응.items():
        if hasattr(implementasi, saat_ini_item): globals()[이전] = getattr(implementasi, saat_ini_item)
