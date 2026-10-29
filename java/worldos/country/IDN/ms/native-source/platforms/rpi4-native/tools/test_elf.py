#!/usr/bin/env python3
"""기존 LALUAN 호환 titik_permulaan. sebenar_data pelaksanaan: ../alat/실행파일시험.py"""
import importlib as TAKE_VALUE
import sys as sistem_pengendalian_VALUE
from pathlib import Path as LALUAN
sistem_pengendalian_VALUE.path.insert(0, str(LALUAN(__file__).resolve().parents[1] / 'alat'))
if __name__ == '__main__':
    import runpy as aplikasi_pelancar
    aplikasi_pelancar.run_module('실행파일시험', run_name='__main__', alter_sys=True)
else:
    pelaksanaan = TAKE_VALUE.import_module('실행파일시험')
    대응 = {'out': 'ukuran_data', 'expected': '예상결과', 'phoff': 'aplikasi_Pengepala_Ofset', 'offset': 'Ofset_VALUE', 'invalid': 'tak_sah_data', 'path': 'LALUAN', 'executable': 'fail_boleh_laku_imej', 'rejected': '거부결과', 'linux_example': '리눅스예제', 'original': '원본', 'result': 'ukuran', 'format_': 'format_b87fd068', 'main': 'Jalan', 'content': 'Kandungan_VALUE', 'source': '원본자료', 'name': 'Nama', 'reference': 'Perbandingan_garis_asas', 'ROOT': 'projek_akar', 'value': 'VALUE', 'report': 'pensahihan_lapor'}
    for 이전, 현재 in 대응.items():
        if hasattr(pelaksanaan, 현재): globals()[이전] = getattr(pelaksanaan, 현재)
