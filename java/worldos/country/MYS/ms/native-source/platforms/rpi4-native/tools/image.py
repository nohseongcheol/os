#!/usr/bin/env python3
"""기존 LALUAN 호환 titik_permulaan. sebenar_data pelaksanaan: ../alat/cipta_imej.py"""
import importlib as TAKE_VALUE
import sys as sistem_pengendalian_VALUE
from pathlib import Path as LALUAN
sistem_pengendalian_VALUE.path.insert(0, str(LALUAN(__file__).resolve().parents[1] / 'alat'))
if __name__ == '__main__':
    import runpy as aplikasi_pelancar
    aplikasi_pelancar.run_module('cipta_imej', run_name='__main__', alter_sys=True)
else:
    pelaksanaan = TAKE_VALUE.import_module('cipta_imej')
    대응 = {'total': '총량', 'start': 'Jalan', 'firmware': '기초제어프로그램', 'files': 'fail_Senarai', 'archive_base': 'Arkib_BASE', 'partition': 'petak_fail', 'archive': 'Arkib', 'main': 'Jalan', 'block': 'blok_data', 'ROOT': 'projek_akar', 'boot': '부팅경로', 'stage': 'pentas_VALUE', 'out': 'ukuran_data', 'expected': '예상결과', 'f': 'fail_pemasukan', 'src': '원본주소', 'path': 'LALUAN', 'p': 'data_jawatan', 'extracted': '추출자료', 'member': 'ahli', 'mbr': 'rekod_but_utama', 'image': 'imej', 'sector_count': '섹터개수', 'dist': '배포경로', 'sha': '해시계산', 'license_': 'lesenkan', 'source': '원본자료', 'name': 'Nama', 'value': 'VALUE', 'manifest': 'pakej_manifes_aplikasi', 'dest': 'destinasi_VALUE_jawatan', 'work': '작업경로'}
    for 이전, 현재 in 대응.items():
        if hasattr(pelaksanaan, 현재): globals()[이전] = getattr(pelaksanaan, 현재)
