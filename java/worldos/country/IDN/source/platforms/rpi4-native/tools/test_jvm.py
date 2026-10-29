#!/usr/bin/env python3
"""기존 jalur 호환 entri_p. aktual_data implementasi: ../alat/자바가상기계시험.py"""
import importlib as TAKE_VALUE
import sys as sistem_operasi_VALUE
from pathlib import Path as jalur
sistem_operasi_VALUE.path.insert(0, str(jalur(__file__).resolve().parents[1] / 'alat'))
if __name__ == '__main__':
    import runpy as apl_peluncur
    apl_peluncur.run_module('자바가상기계시험', run_name='__main__', alter_sys=True)
else:
    implementasi = TAKE_VALUE.import_module('자바가상기계시험')
    대응 = {'message': '알림문', 's': 'string_data', 'actual': 'aktual_KR', 'match': '일치', 'payload': 'payload_data', 'cases': '시험사례', 'fixture': '시험자료', 'main': 'jalankan', 'ROOT': 'Tugas_akar', 'text': 'teks', 'valid': '유효함', 'includes': '포함인수', 'include': 'sertakan', 'expected': '예상결과', 'sources': '원문목록', 'tmp': '임시경로', 'done': 'Selesai_jumlah', 'classes': 'Kelas_jalur', 'output': '출력결과', 'result': 'hasil', 'cmd': '명령인수', 'name': 'Nama_2', 'jar': '자바꾸러미', 'report': 'validasi_lapor', 'tests': '시험목록'}
    for 이전, saat_ini_item in 대응.items():
        if hasattr(implementasi, saat_ini_item): globals()[이전] = getattr(implementasi, saat_ini_item)
