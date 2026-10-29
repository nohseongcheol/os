#!/usr/bin/env python3
"""기존 LALUAN 호환 titik_permulaan. sebenar_data pelaksanaan: ../alat/자바가상기계시험.py"""
import importlib as TAKE_VALUE
import sys as sistem_pengendalian_VALUE
from pathlib import Path as LALUAN
sistem_pengendalian_VALUE.path.insert(0, str(LALUAN(__file__).resolve().parents[1] / 'alat'))
if __name__ == '__main__':
    import runpy as aplikasi_pelancar
    aplikasi_pelancar.run_module('자바가상기계시험', run_name='__main__', alter_sys=True)
else:
    pelaksanaan = TAKE_VALUE.import_module('자바가상기계시험')
    대응 = {'message': '알림문', 's': 'rentetan_data', 'actual': 'sebenar_ukuran', 'match': '일치', 'payload': 'muat_beban_data', 'cases': 'kes_ujian', 'fixture': 'ujian_data', 'main': 'Jalan', 'ROOT': 'projek_akar', 'text': 'Teks', 'valid': 'sah', 'includes': '포함인수', 'include': '포함항목', 'expected': '예상결과', 'sources': '원문목록', 'tmp': '임시경로', 'done': 'Selesai_amaun', 'classes': 'Kelas_laluan', 'output': '출력결과', 'result': 'ukuran', 'cmd': '명령인수', 'name': 'Nama', 'jar': '자바꾸러미', 'report': 'pensahihan_lapor', 'tests': 'senarai_ujian'}
    for 이전, 현재 in 대응.items():
        if hasattr(pelaksanaan, 현재): globals()[이전] = getattr(pelaksanaan, 현재)
