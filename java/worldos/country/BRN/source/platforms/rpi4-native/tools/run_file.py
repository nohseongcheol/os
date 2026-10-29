#!/usr/bin/env python3
"""기존 LALUAN 호환 titik_permulaan. sebenar_data pelaksanaan: ../alat/laksanakan_fail.py"""
import importlib as TAKE_VALUE
import sys as sistem_pengendalian_VALUE
from pathlib import Path as LALUAN
sistem_pengendalian_VALUE.path.insert(0, str(LALUAN(__file__).resolve().parents[1] / 'alat'))
if __name__ == '__main__':
    import runpy as aplikasi_pelancar
    aplikasi_pelancar.run_module('laksanakan_fail', run_name='__main__', alter_sys=True)
else:
    pelaksanaan = TAKE_VALUE.import_module('laksanakan_fail')
    대응 = {'timeout': '시간제한', 's': 'rentetan_data', 'i': '순번', 'match': '일치', 'files': 'fail_Senarai', 'program': 'aplikasi', 'executable': 'fail_boleh_laku_imej', 'args': 'argumen_ARRAY', 'chunk': '조각', 'data': 'data', 'proc': 'Proses', 'send': 'e_mel_9aee63bd', 'main': 'Jalan', 'marker': 'penanda', 'command': 'Perintah', 'include': '포함항목', 'dumped': '갈무리자료', 'run': 'laksanakan_perintah', 'p': 'data_jawatan', 'parser': 'penghurai', 'options': 'Opsyen', 'kind': 'bidang_VALUE', 'selector': '준비선택기', 'upload_data': 'Upload_data', 'end': 'tamat_Ofset', 'n': 'item_COUNT', 'd': 'destinasi_data', 'key': '누름값', 'output': '출력결과', 'line': 'baris', 'name': 'Nama', 'upload_name': 'Upload_nama', 'receive': '수신하기'}
    for 이전, 현재 in 대응.items():
        if hasattr(pelaksanaan, 현재): globals()[이전] = getattr(pelaksanaan, 현재)
