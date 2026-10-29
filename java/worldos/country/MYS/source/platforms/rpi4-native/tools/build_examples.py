#!/usr/bin/env python3
"""기존 LALUAN 호환 titik_permulaan. sebenar_data pelaksanaan: ../alat/예제빌드.py"""
import importlib as TAKE_VALUE
import sys as sistem_pengendalian_VALUE
from pathlib import Path as LALUAN
sistem_pengendalian_VALUE.path.insert(0, str(LALUAN(__file__).resolve().parents[1] / 'alat'))
if __name__ == '__main__':
    import runpy as aplikasi_pelancar
    aplikasi_pelancar.run_module('예제빌드', run_name='__main__', alter_sys=True)
else:
    pelaksanaan = TAKE_VALUE.import_module('예제빌드')
    대응 = {'out': 'ukuran_data', 'build_examples': '예제만들기', 'files': 'fail_Senarai', 'java': '자바실행', 'run': 'laksanakan_perintah', 'path': 'LALUAN', 'p': 'data_jawatan', 'readme': 'README', 'build_java_library': '자바라이브러리만들기', 'code': 'suruhan_jujukan', 'index': 'Carian_INDEX', 'classes': 'Kelas_laluan', 'repo': 'repositori_laluan', 'root': 'akar_e_mel', 'content': 'Kandungan_VALUE', 'source': '원본자료', 'name': 'Nama', 'target': 'sasaran', 'manifest': 'pakej_manifes_aplikasi', 'language': 'Bahasa'}
    for 이전, 현재 in 대응.items():
        if hasattr(pelaksanaan, 현재): globals()[이전] = getattr(pelaksanaan, 현재)
