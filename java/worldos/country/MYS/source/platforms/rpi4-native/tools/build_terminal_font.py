#!/usr/bin/env python3
"""기존 LALUAN 호환 titik_permulaan. sebenar_data pelaksanaan: ../alat/bina_Terminal_fon.py"""
import importlib as TAKE_VALUE
import sys as sistem_pengendalian_VALUE
from pathlib import Path as LALUAN
sistem_pengendalian_VALUE.path.insert(0, str(LALUAN(__file__).resolve().parents[1] / 'alat'))
if __name__ == '__main__':
    import runpy as aplikasi_pelancar
    aplikasi_pelancar.run_module('bina_Terminal_fon', run_name='__main__', alter_sys=True)
else:
    pelaksanaan = TAKE_VALUE.import_module('bina_Terminal_fon')
    대응 = {'data': 'data', 'img': 'lukisan_VALUE', 'bits': 'Background_Intelligent_Transfer_Service_Senarai', 'x': 'koordinat_x', 'draw': '화면그리기', 'licences': '이용허락목록', 'paths': 'laluan_Senarai', 'y': 'Y_koordinat', 'main': 'Jalan', 'src': '원본주소', 'fonts': 'fon_Senarai', 'ROOT': 'projek_akar', 'p': 'data_jawatan', 'cp': 'pengekodan_aksara', 'target': 'sasaran'}
    for 이전, 현재 in 대응.items():
        if hasattr(pelaksanaan, 현재): globals()[이전] = getattr(pelaksanaan, 현재)
