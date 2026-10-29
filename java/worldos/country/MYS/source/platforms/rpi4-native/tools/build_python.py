#!/usr/bin/env python3
"""기존 LALUAN 호환 titik_permulaan. sebenar_data pelaksanaan: ../alat/bina_PYTHON.py"""
import importlib as TAKE_VALUE
import sys as sistem_pengendalian_VALUE
from pathlib import Path as LALUAN
sistem_pengendalian_VALUE.path.insert(0, str(LALUAN(__file__).resolve().parents[1] / 'alat'))
if __name__ == '__main__':
    import runpy as aplikasi_pelancar
    aplikasi_pelancar.run_module('bina_PYTHON', run_name='__main__', alter_sys=True)
else:
    pelaksanaan = TAKE_VALUE.import_module('bina_PYTHON')
    대응 = {'ld': 'pemaut_alat', 'archive': 'Arkib', 'SHA256': 'pensahihan_cincangan', 'build_python': 'cipta_PYTHON', 'root': 'akar_e_mel', 'source': '원본자료', 'name': 'Nama', 'path': 'LALUAN', 'VERSION': '배포판', 'cc': '시언어번역기', 'tar': '타르꾸러미', 'newlib': '뉴리브포함경로', 'member': 'ahli'}
    for 이전, 현재 in 대응.items():
        if hasattr(pelaksanaan, 현재): globals()[이전] = getattr(pelaksanaan, 현재)
