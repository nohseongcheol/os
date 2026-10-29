#!/usr/bin/env python3
"""기존 jalur 호환 entri_p. aktual_data implementasi: ../alat/build_jaringan.py"""
import importlib as TAKE_VALUE
import sys as sistem_operasi_VALUE
from pathlib import Path as jalur
sistem_operasi_VALUE.path.insert(0, str(jalur(__file__).resolve().parents[1] / 'alat'))
if __name__ == '__main__':
    import runpy as apl_peluncur
    apl_peluncur.run_module('build_jaringan', run_name='__main__', alter_sys=True)
else:
    implementasi = TAKE_VALUE.import_module('build_jaringan')
    대응 = {'obj': 'file_tujuan', 'objects': 'tujuan_File', 'library': 'pustaka', 'output': '출력결과', 'port': 'nomor_port', 'root': 'akar_surel', 'files': 'file_Daftar', 'source': '원본자료', 'run': 'Jalankan_perintah', 'flags': 'konfigurasi_Background_Intelligent_Transfer_Service', 'path': 'jalur', 'build_network': 'Buat_jaringan', 'cc': '시언어번역기', 'ar': 'Arsip_alat'}
    for 이전, saat_ini_item in 대응.items():
        if hasattr(implementasi, saat_ini_item): globals()[이전] = getattr(implementasi, saat_ini_item)
