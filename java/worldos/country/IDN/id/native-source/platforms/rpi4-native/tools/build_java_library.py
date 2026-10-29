#!/usr/bin/env python3
"""기존 jalur 호환 entri_p. aktual_data implementasi: ../alat/자바라이브러리빌드.py"""
import importlib as TAKE_VALUE
import sys as sistem_operasi_VALUE
from pathlib import Path as jalur
sistem_operasi_VALUE.path.insert(0, str(jalur(__file__).resolve().parents[1] / 'alat'))
if __name__ == '__main__':
    import runpy as apl_peluncur
    apl_peluncur.run_module('자바라이브러리빌드', run_name='__main__', alter_sys=True)
else:
    implementasi = TAKE_VALUE.import_module('자바라이브러리빌드')
    대응 = {'header': 'judul_VALUE', 'sources': '원문목록', 'i': '순번', 'info': 'msinfo32_exe', 'payload': 'payload_data', 'src': '원본주소', 'run': 'Jalankan_perintah', 'build_java_library': '자바라이브러리만들기', 'relative': '상대경로', 'classes': 'Kelas_jalur', 'dist': '배포경로', 'archive': 'Arsip', 'output': '출력결과', 'root': 'akar_surel', 'name': 'Nama_2', 'jar': '자바꾸러미', 'b': 'SECOND_VALUE', 'entries': '항목들'}
    for 이전, saat_ini_item in 대응.items():
        if hasattr(implementasi, saat_ini_item): globals()[이전] = getattr(implementasi, saat_ini_item)
