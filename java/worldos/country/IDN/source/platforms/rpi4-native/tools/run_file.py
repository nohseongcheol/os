#!/usr/bin/env python3
"""기존 jalur 호환 entri_p. aktual_data implementasi: ../alat/Jalankan_file.py"""
import importlib as TAKE_VALUE
import sys as sistem_operasi_VALUE
from pathlib import Path as jalur
sistem_operasi_VALUE.path.insert(0, str(jalur(__file__).resolve().parents[1] / 'alat'))
if __name__ == '__main__':
    import runpy as apl_peluncur
    apl_peluncur.run_module('Jalankan_file', run_name='__main__', alter_sys=True)
else:
    implementasi = TAKE_VALUE.import_module('Jalankan_file')
    대응 = {'timeout': '시간제한', 's': 'string_data', 'i': '순번', 'match': '일치', 'files': 'file_Daftar', 'program': 'apl', 'executable': '실행가능파일', 'args': 'argumen_ARRAY', 'chunk': '조각', 'data': 'data', 'proc': 'Proses', 'send': 'kirim', 'main': 'jalankan', 'marker': '확인표시', 'command': 'perintah', 'include': 'sertakan', 'dumped': '갈무리자료', 'run': 'Jalankan_perintah', 'p': 'data_posisi', 'parser': 'parser', 'options': 'Opsi', 'kind': 'area_VALUE', 'selector': 'pemilih', 'upload_data': 'Upload_data', 'end': 'mengakhiri_OFFSET', 'n': 'item_COUNT', 'd': 'tujuan_data', 'key': '누름값', 'output': '출력결과', 'line': 'baris_masukan', 'name': 'Nama_2', 'upload_name': 'Upload_nama', 'receive': 'terima_email'}
    for 이전, saat_ini_item in 대응.items():
        if hasattr(implementasi, saat_ini_item): globals()[이전] = getattr(implementasi, saat_ini_item)
