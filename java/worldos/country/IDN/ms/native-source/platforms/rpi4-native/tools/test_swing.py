#!/usr/bin/env python3
"""기존 LALUAN 호환 titik_permulaan. sebenar_data pelaksanaan: ../alat/화면요소시험.py"""
import importlib as TAKE_VALUE
import sys as sistem_pengendalian_VALUE
from pathlib import Path as LALUAN
sistem_pengendalian_VALUE.path.insert(0, str(LALUAN(__file__).resolve().parents[1] / 'alat'))
if __name__ == '__main__':
    import runpy as aplikasi_pelancar
    aplikasi_pelancar.run_module('화면요소시험', run_name='__main__', alter_sys=True)
else:
    pelaksanaan = TAKE_VALUE.import_module('화면요소시험')
    대응 = {'wait': '기다리기', 'x': 'koordinat_x', 's': 'rentetan_data', 'i': '순번', 'sel': '선택기', 'seconds': '초단위', 'log': 'LOG_baris', 'data': 'data', 'at': '현재위치', 'send': 'e_mel_9aee63bd', 'main': 'Jalan', 'req': 'permintaan_VALUE', 'hot': 'pintasan_VALUE', 'pump': 'pemegang_acara', 'ROOT': 'projek_akar', 'marker': 'penanda', 'b': 'SECOND_VALUE', 'command': 'Perintah', 'shell': 'cangkerang', 'f': 'fail_pemasukan', 'click': 'klik_butang', 'k': '셋째순번', 'c': 'titik_kod', 'r': '반환값', 'p': 'data_jawatan', 'command_mode': 'perintah_mod', 'end': 'tamat_Ofset', 'classes': 'Kelas_laluan', 'key': '누름값', 'y': 'Y_koordinat', 'result': 'ukuran', 'report': 'pensahihan_lapor', 'dest': 'destinasi_VALUE_jawatan', 'work': '작업경로', 'qmp': '모의제어접속'}
    for 이전, 현재 in 대응.items():
        if hasattr(pelaksanaan, 현재): globals()[이전] = getattr(pelaksanaan, 현재)
