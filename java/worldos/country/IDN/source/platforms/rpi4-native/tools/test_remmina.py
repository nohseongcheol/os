#!/usr/bin/env python3
"""기존 jalur 호환 entri_p. aktual_data implementasi: ../alat/원격한글시험.py"""
import importlib as TAKE_VALUE
import sys as sistem_operasi_VALUE
from pathlib import Path as jalur
sistem_operasi_VALUE.path.insert(0, str(jalur(__file__).resolve().parents[1] / 'alat'))
if __name__ == '__main__':
    import runpy as apl_peluncur
    apl_peluncur.run_module('원격한글시험', run_name='__main__', alter_sys=True)
else:
    implementasi = TAKE_VALUE.import_module('원격한글시험')
    대응 = {'wait': '기다리기', 'typing': '글자입력', 'start': 'jalankan', 'profile': 'Profil', 'focused': 'Prioritas', 'serial': '직렬입출력', 'keys': '누름열', 'server': 'server_VALUE', 'log': 'LOG_baris', 'args': 'argumen_ARRAY', 'deadline': 'tenggat_waktu_TIME', 'data': 'data', 'candidate': '후보', 'logs': '기록들', 'kw': 'argumen_bernama', 'number': '수치', 'main': 'jalankan', 'ready': '준비완료', 'found': 'Cari_KR', 'guest': 'tamu', 'ROOT': 'Tugas_akar', 'marker': '확인표시', 'text': 'teks', 'out': 'KR_data', 'env': 'lingkungan', 'f': 'file_entri', 'port': 'nomor_port', 'offset': 'OFFSET_VALUE', 'version': 'nomor_versi', 'p': 'data_posisi', 'selector': 'pemilih', 'xvfb': 'maya_tampilan', 'display': 'tampilan', 'n': 'item_COUNT', 'key': '누름값', 'processes': '실행과정들', 'rootfs': '뿌리파일계층', 'xdo': '가상입력도구', 'name': 'Nama_2', 'window': 'Jendela', 'report': 'validasi_lapor', 'work': '작업경로'}
    for 이전, saat_ini_item in 대응.items():
        if hasattr(implementasi, saat_ini_item): globals()[이전] = getattr(implementasi, saat_ini_item)
