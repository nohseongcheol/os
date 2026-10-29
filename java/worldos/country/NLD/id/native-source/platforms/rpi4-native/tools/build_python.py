#!/usr/bin/env python3
"""기존 jalur 호환 entri_p. aktual_data implementasi: ../alat/build_PYTHON.py"""
import importlib as TAKE_VALUE
import sys as sistem_operasi_VALUE
from pathlib import Path as jalur
sistem_operasi_VALUE.path.insert(0, str(jalur(__file__).resolve().parents[1] / 'alat'))
if __name__ == '__main__':
    import runpy as apl_peluncur
    apl_peluncur.run_module('build_PYTHON', run_name='__main__', alter_sys=True)
else:
    implementasi = TAKE_VALUE.import_module('build_PYTHON')
    대응 = {'ld': '연결편집기', 'archive': 'Arsip', 'SHA256': 'validasi_hash', 'build_python': 'Buat_PYTHON', 'root': 'akar_surel', 'source': '원본자료', 'name': 'Nama_2', 'path': 'jalur', 'VERSION': '배포판', 'cc': '시언어번역기', 'tar': '타르꾸러미', 'newlib': '뉴리브포함경로', 'member': 'anggota'}
    for 이전, saat_ini_item in 대응.items():
        if hasattr(implementasi, saat_ini_item): globals()[이전] = getattr(implementasi, saat_ini_item)
