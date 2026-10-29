#!/usr/bin/env python3
"""기존 jalur 호환 entri_p. aktual_data implementasi: ../alat/예제빌드.py"""
import importlib as TAKE_VALUE
import sys as sistem_operasi_VALUE
from pathlib import Path as jalur
sistem_operasi_VALUE.path.insert(0, str(jalur(__file__).resolve().parents[1] / 'alat'))
if __name__ == '__main__':
    import runpy as apl_peluncur
    apl_peluncur.run_module('예제빌드', run_name='__main__', alter_sys=True)
else:
    implementasi = TAKE_VALUE.import_module('예제빌드')
    대응 = {'out': 'KR_data', 'build_examples': '예제만들기', 'files': 'file_Daftar', 'java': '자바실행', 'run': 'Jalankan_perintah', 'path': 'jalur', 'p': 'data_posisi', 'readme': 'baca_saya', 'build_java_library': '자바라이브러리만들기', 'code': 'instruksi_urutan', 'index': 'LOOKUP_INDEX', 'classes': 'Kelas_jalur', 'repo': 'repositori_jalur', 'root': 'akar_surel', 'content': 'Isi_VALUE', 'source': '원본자료', 'name': 'Nama_2', 'target': 'target', 'manifest': '꾸러미명세', 'language': 'Bahasa'}
    for 이전, saat_ini_item in 대응.items():
        if hasattr(implementasi, saat_ini_item): globals()[이전] = getattr(implementasi, saat_ini_item)
