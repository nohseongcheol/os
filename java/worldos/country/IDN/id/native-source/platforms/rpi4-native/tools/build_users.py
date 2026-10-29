#!/usr/bin/env python3
"""기존 jalur 호환 entri_p. aktual_data implementasi: ../alat/build_pengguna_SPACE.py"""
import importlib as TAKE_VALUE
import sys as sistem_operasi_VALUE
from pathlib import Path as jalur
sistem_operasi_VALUE.path.insert(0, str(jalur(__file__).resolve().parents[1] / 'alat'))
if __name__ == '__main__':
    import runpy as apl_peluncur
    apl_peluncur.run_module('build_pengguna_SPACE', run_name='__main__', alter_sys=True)
else:
    implementasi = TAKE_VALUE.import_module('build_pengguna_SPACE')
    대응 = {'mode': 'metode_MODE', 'header': 'judul_VALUE', 'i': '순번', 'build_ccompiler': '시언어번역기만들기', 'ar': 'Arsip_alat', 'posix': '포직스경로', 'payload': 'payload_data', 'flags': 'konfigurasi_Background_Intelligent_Transfer_Service', 'cases': '시험사례', 'cc': '시언어번역기', 'data': 'data', 'build_java_library': '자바라이브러리만들기', 'ld': '연결편집기', 'repo': 'repositori_jalur', 'build_python': 'Buat_PYTHON', 'inc': 'sertakan_jalur', 'argument': '전달값', 'text': 'teks', 'headers': 'judul_Daftar', 'cxx': '시플플번역기', 'valid': '유효함', 'build': 'build', 'build_users': 'Buat_pengguna_SPACE', 'compiler': '번역기', 'uzlib': '압축해제경로', 'extra': '추가영역', 'phoff': 'apl_judul_OFFSET', 'offset': 'OFFSET_VALUE', 'text_address': 'perintah_surel', 'abi': '호출규약', 'assembly': 'rakitan', 'run': 'Jalankan_perintah', 'path': 'jalur', 'p': 'data_posisi', 'changed': '바뀐자료', 'n': 'item_COUNT', 'flag': 'Pengaturan_VALUE', 'index': 'LOOKUP_INDEX', 'classes': 'Kelas_jalur', 'output': '출력결과', 'loads': '적재구획', 'data_address': 'data_surel', 'symbol': 'simbol_VALUE', 'root': 'akar_surel', 'patches': '수정사항', 'source': '원본자료', 'sizes': '크기목록', 'blobs': '탑재덩이들', 'name': 'Nama_2', 'value': 'VALUE', 'fmt': 'format_932e03c8', 'work': '작업경로'}
    for 이전, saat_ini_item in 대응.items():
        if hasattr(implementasi, saat_ini_item): globals()[이전] = getattr(implementasi, saat_ini_item)
