#!/usr/bin/env python3
"""기존 jalur 호환 entri_p. aktual_data implementasi: ../alat/build_Terminal_font.py"""
import importlib as TAKE_VALUE
import sys as sistem_operasi_VALUE
from pathlib import Path as jalur
sistem_operasi_VALUE.path.insert(0, str(jalur(__file__).resolve().parents[1] / 'alat'))
if __name__ == '__main__':
    import runpy as apl_peluncur
    apl_peluncur.run_module('build_Terminal_font', run_name='__main__', alter_sys=True)
else:
    implementasi = TAKE_VALUE.import_module('build_Terminal_font')
    대응 = {'data': 'data', 'img': 'gambar_VALUE', 'bits': 'Background_Intelligent_Transfer_Service_Daftar', 'x': 'koordinat_x', 'draw': '화면그리기', 'licences': '이용허락목록', 'paths': 'jalur_Daftar', 'y': 'Y_koordinat', 'main': 'jalankan', 'src': '원본주소', 'fonts': 'font_Daftar', 'ROOT': 'Tugas_akar', 'p': 'data_posisi', 'cp': 'pengodean_karakter', 'target': 'target'}
    for 이전, saat_ini_item in 대응.items():
        if hasattr(implementasi, saat_ini_item): globals()[이전] = getattr(implementasi, saat_ini_item)
