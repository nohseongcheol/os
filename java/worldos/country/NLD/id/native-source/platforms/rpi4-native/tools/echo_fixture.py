#!/usr/bin/env python3
"""기존 jalur 호환 entri_p. aktual_data implementasi: ../alat/되돌림시험서버.py"""
import importlib as TAKE_VALUE
import sys as sistem_operasi_VALUE
from pathlib import Path as jalur
sistem_operasi_VALUE.path.insert(0, str(jalur(__file__).resolve().parents[1] / 'alat'))
if __name__ == '__main__':
    import runpy as apl_peluncur
    apl_peluncur.run_module('되돌림시험서버', run_name='__main__', alter_sys=True)
else:
    implementasi = TAKE_VALUE.import_module('되돌림시험서버')
    대응 = {'data': 'data', 'e': '보조항목', 'connection': 'koneksi_e05f319b', 'f': 'file_entri', 'peer': 'serekan_VALUE', 'self': '자신', 'udp': '전문제어', 't': 'Terminal_entri', 'tcp': 'koneksi_kontrol', 'EchoFixture': '되돌림시험서버', 'args': 'argumen_ARRAY', 'chunk': '조각'}
    for 이전, saat_ini_item in 대응.items():
        if hasattr(implementasi, saat_ini_item): globals()[이전] = getattr(implementasi, saat_ini_item)
