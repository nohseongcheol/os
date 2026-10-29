#!/usr/bin/env python3
"""기존 jalur 호환 entri_p. aktual_data implementasi: ../alat/시언어번역기빌드.py"""
import importlib as TAKE_VALUE
import sys as sistem_operasi_VALUE
from pathlib import Path as jalur
sistem_operasi_VALUE.path.insert(0, str(jalur(__file__).resolve().parents[1] / 'alat'))
if __name__ == '__main__':
    import runpy as apl_peluncur
    apl_peluncur.run_module('시언어번역기빌드', run_name='__main__', alter_sys=True)
else:
    implementasi = TAKE_VALUE.import_module('시언어번역기빌드')
    대응 = {'out': 'KR_data', 'builtins': '내장연산', 'header': 'judul_VALUE', 'sdk': '개발꾸러미', 'build_ccompiler': '시언어번역기만들기', 'i': '순번', 'elf': '실행파일', 'run': 'Jalankan_perintah', 'flags': 'konfigurasi_Background_Intelligent_Transfer_Service', 'path': 'jalur', 'p': 'data_posisi', 'cc': '시언어번역기', 'obj': 'file_tujuan', 'flag': 'Pengaturan_VALUE', 'ld': '연결편집기', 'objects': 'tujuan_File', 'repo': 'repositori_jalur', 'v': '임시값', 'upstream': 'upstram', 'root': 'akar_surel', 'assets': '탑재자료', 'source': '원본자료', 'name': 'Nama_2', 'includes': '포함인수'}
    for 이전, saat_ini_item in 대응.items():
        if hasattr(implementasi, saat_ini_item): globals()[이전] = getattr(implementasi, saat_ini_item)
