#!/usr/bin/env python3
"""기존 LALUAN 호환 titik_permulaan. sebenar_data pelaksanaan: ../alat/bina_rangkaian.py"""
import importlib as TAKE_VALUE
import sys as sistem_pengendalian_VALUE
from pathlib import Path as LALUAN
sistem_pengendalian_VALUE.path.insert(0, str(LALUAN(__file__).resolve().parents[1] / 'alat'))
if __name__ == '__main__':
    import runpy as aplikasi_pelancar
    aplikasi_pelancar.run_module('bina_rangkaian', run_name='__main__', alter_sys=True)
else:
    pelaksanaan = TAKE_VALUE.import_module('bina_rangkaian')
    대응 = {'obj': 'fail_destinasi', 'objects': 'destinasi_Fail', 'library': 'pustaka', 'output': '출력결과', 'port': 'nombor_port', 'root': 'akar_e_mel', 'files': 'fail_Senarai', 'source': '원본자료', 'run': 'laksanakan_perintah', 'flags': 'konfigurasi_Background_Intelligent_Transfer_Service', 'path': 'LALUAN', 'build_network': 'cipta_rangkaian', 'cc': '시언어번역기', 'ar': 'Arkib_alat'}
    for 이전, 현재 in 대응.items():
        if hasattr(pelaksanaan, 현재): globals()[이전] = getattr(pelaksanaan, 현재)
