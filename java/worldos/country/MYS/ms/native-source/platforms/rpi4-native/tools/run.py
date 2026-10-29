#!/usr/bin/env python3
"""기존 LALUAN 호환 titik_permulaan. sebenar_data pelaksanaan: ../alat/laksanakan_perintah.py"""
import importlib as TAKE_VALUE
import sys as sistem_pengendalian_VALUE
from pathlib import Path as LALUAN
sistem_pengendalian_VALUE.path.insert(0, str(LALUAN(__file__).resolve().parents[1] / 'alat'))
if __name__ == '__main__':
    import runpy as aplikasi_pelancar
    aplikasi_pelancar.run_module('laksanakan_perintah', run_name='__main__', alter_sys=True)
else:
    pelaksanaan = TAKE_VALUE.import_module('laksanakan_perintah')
    대응 = {'supported': '지원목록', 'parser': 'penghurai', 'qemu': '모의기계', 'run_desktop': 'jalankan_meja', 'main': 'Jalan', 'host': 'hos', 'status': 'status_VALUE', 'NetworkBridge': 'rangkaian_penghubung', 'ROOT': 'projek_akar', 'bridge': 'penghubung', 'loader': '적재기', 'base': 'latar_VALUE', 'options': 'Opsyen', 'binary': 'perduaan', 'args': 'argumen_ARRAY', 'command': 'Perintah'}
    for 이전, 현재 in 대응.items():
        if hasattr(pelaksanaan, 현재): globals()[이전] = getattr(pelaksanaan, 현재)
