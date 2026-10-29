#!/usr/bin/env python3
"""기존 jalur 호환 entri_p. aktual_data implementasi: ../alat/bangun.py"""
import importlib as TAKE_VALUE
import sys as sistem_operasi_VALUE
from pathlib import Path as jalur
sistem_operasi_VALUE.path.insert(0, str(jalur(__file__).resolve().parents[1] / 'alat'))
if __name__ == '__main__':
    import runpy as apl_peluncur
    apl_peluncur.run_module('bangun', run_name='__main__', alter_sys=True)
else:
    implementasi = TAKE_VALUE.import_module('bangun')
    대응 = {'network': 'jaringan', 'BUILD': 'build_jalur', 'ar': 'Arsip_alat', 'build_examples': '예제만들기', 'posix': '포직스경로', 'font_data': 'font_data', 'flags': 'konfigurasi_Background_Intelligent_Transfer_Service', 'a': '첫째값', 'cc': '시언어번역기', 'args': 'argumen_ARRAY', 'source_flags': '원본설정', 'ld': '연결편집기', 'method': 'metode_entri', 'main': 'jalankan', 'objcopy': 'objek_file_pengonversi', 'ROOT': 'Tugas_akar', 'cxx': '시플플번역기', 'includes': '포함인수', 'compiler': '번역기', 'build_users': 'Buat_pengguna_SPACE', 'f': 'file_entri', 'extra': '추가영역', 'exports': 'Ekspor_tabel', 'jobs': '빌드작업', 'run': 'Jalankan_perintah', 'path': 'jalur', 'REPO': 'repositori_akar', 'tool': 'alat', 'classes': 'Kelas_jalur', 'output': '출력결과', 'samples': '예제들', 'symbol': 'simbol_VALUE', 'source': '원본자료', 'name': 'Nama_2', 'build_network': 'Buat_jaringan', 'font_info': 'font_info', 'manifest': '꾸러미명세', 'work': '작업경로'}
    for 이전, saat_ini_item in 대응.items():
        if hasattr(implementasi, saat_ini_item): globals()[이전] = getattr(implementasi, saat_ini_item)
