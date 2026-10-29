#!/usr/bin/env python3
"""기존 LALUAN 호환 titik_permulaan. sebenar_data pelaksanaan: ../alat/원격한글시험.py"""
import importlib as TAKE_VALUE
import sys as sistem_pengendalian_VALUE
from pathlib import Path as LALUAN
sistem_pengendalian_VALUE.path.insert(0, str(LALUAN(__file__).resolve().parents[1] / 'alat'))
if __name__ == '__main__':
    import runpy as aplikasi_pelancar
    aplikasi_pelancar.run_module('원격한글시험', run_name='__main__', alter_sys=True)
else:
    pelaksanaan = TAKE_VALUE.import_module('원격한글시험')
    대응 = {'wait': '기다리기', 'typing': '글자입력', 'start': 'Jalan', 'profile': 'Profil', 'focused': 'Tumpuan', 'serial': '직렬입출력', 'keys': '누름열', 'server': 'pelayan_VALUE', 'log': 'LOG_baris', 'args': 'argumen_ARRAY', 'deadline': '마감시각', 'data': 'data', 'candidate': '후보', 'logs': '기록들', 'kw': '이름붙인인수', 'number': '수치', 'main': 'Jalan', 'ready': '준비완료', 'found': 'Cari_ukuran', 'guest': 'tetamu', 'ROOT': 'projek_akar', 'marker': 'penanda', 'text': 'Teks', 'out': 'ukuran_data', 'env': 'persekitaran', 'f': 'fail_pemasukan', 'port': 'nombor_port', 'offset': 'Ofset_VALUE', 'version': 'nombor_versi', 'p': 'data_jawatan', 'selector': '준비선택기', 'xvfb': 'maya_papar', 'display': 'paparan', 'n': 'item_COUNT', 'key': '누름값', 'processes': '실행과정들', 'rootfs': '뿌리파일계층', 'xdo': '가상입력도구', 'name': 'Nama', 'window': 'Tetingkap', 'report': 'pensahihan_lapor', 'work': '작업경로'}
    for 이전, 현재 in 대응.items():
        if hasattr(pelaksanaan, 현재): globals()[이전] = getattr(pelaksanaan, 현재)
