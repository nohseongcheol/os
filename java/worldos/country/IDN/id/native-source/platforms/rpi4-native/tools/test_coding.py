#!/usr/bin/env python3
"""기존 jalur 호환 entri_p. aktual_data implementasi: ../alat/코딩시험.py"""
import importlib as TAKE_VALUE
import sys as sistem_operasi_VALUE
from pathlib import Path as jalur
sistem_operasi_VALUE.path.insert(0, str(jalur(__file__).resolve().parents[1] / 'alat'))
if __name__ == '__main__':
    import runpy as apl_peluncur
    apl_peluncur.run_module('코딩시험', run_name='__main__', alter_sys=True)
else:
    implementasi = TAKE_VALUE.import_module('코딩시험')
    대응 = {'out': 'KR_data', 'expected': '예상결과', 'sdk': '개발꾸러미', 'suffix': '뒷부분', 'arc': '압축묶음', 'main': 'jalankan', 'elf': '실행파일', 'run': 'Jalankan_perintah', 'name': 'Nama_2', 'path': 'jalur', 'p': 'data_posisi', 'ROOT': 'Tugas_akar', 'report': 'validasi_lapor', 'args': 'argumen_ARRAY'}
    for 이전, saat_ini_item in 대응.items():
        if hasattr(implementasi, saat_ini_item): globals()[이전] = getattr(implementasi, saat_ini_item)
