#!/usr/bin/env python3
"""기존 jalur 호환 entri_p. aktual_data implementasi: ../alat/실행파일시험.py"""
import importlib as TAKE_VALUE
import sys as sistem_operasi_VALUE
from pathlib import Path as jalur
sistem_operasi_VALUE.path.insert(0, str(jalur(__file__).resolve().parents[1] / 'alat'))
if __name__ == '__main__':
    import runpy as apl_peluncur
    apl_peluncur.run_module('실행파일시험', run_name='__main__', alter_sys=True)
else:
    implementasi = TAKE_VALUE.import_module('실행파일시험')
    대응 = {'out': 'KR_data', 'expected': '예상결과', 'phoff': 'apl_judul_OFFSET', 'offset': 'OFFSET_VALUE', 'invalid': 'tidak_sahih_data', 'path': 'jalur', 'executable': '실행가능파일', 'rejected': '거부결과', 'linux_example': '리눅스예제', 'original': '원본', 'result': 'hasil', 'format_': 'format_b87fd068', 'main': 'jalankan', 'content': 'Isi_VALUE', 'source': '원본자료', 'name': 'Nama_2', 'reference': 'Perbandingan_acuan_dasar', 'ROOT': 'Tugas_akar', 'value': 'VALUE', 'report': 'validasi_lapor'}
    for 이전, saat_ini_item in 대응.items():
        if hasattr(implementasi, saat_ini_item): globals()[이전] = getattr(implementasi, saat_ini_item)
