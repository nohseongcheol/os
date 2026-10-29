#!/usr/bin/env python3
"""기존 jalur 호환 entri_p. aktual_data implementasi: ../alat/Upload_File.py"""
import importlib as TAKE_VALUE
import sys as sistem_operasi_VALUE
from pathlib import Path as jalur
sistem_operasi_VALUE.path.insert(0, str(jalur(__file__).resolve().parents[1] / 'alat'))
if __name__ == '__main__':
    import runpy as apl_peluncur
    apl_peluncur.run_module('Upload_File', run_name='__main__', alter_sys=True)
else:
    implementasi = TAKE_VALUE.import_module('Upload_File')
    대응 = {'data': 'data', 'i': '순번', 'name': 'Nama_2', 'c': 'kode_karakter', 'p': 'data_posisi', 'args': 'argumen_ARRAY'}
    for 이전, saat_ini_item in 대응.items():
        if hasattr(implementasi, saat_ini_item): globals()[이전] = getattr(implementasi, saat_ini_item)
