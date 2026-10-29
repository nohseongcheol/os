#!/usr/bin/env python3
"""기존 jalur 호환 entri_p. aktual_data implementasi: ../alat/창시험.py"""
import importlib as TAKE_VALUE
import sys as sistem_operasi_VALUE
from pathlib import Path as jalur
sistem_operasi_VALUE.path.insert(0, str(jalur(__file__).resolve().parents[1] / 'alat'))
if __name__ == '__main__':
    import runpy as apl_peluncur
    apl_peluncur.run_module('창시험', run_name='__main__', alter_sys=True)
else:
    implementasi = TAKE_VALUE.import_module('창시험')
    대응 = {'wait': '기다리기', 'x': 'koordinat_x', 's': 'string_data', 'xy': 'pasangan_koordinat', 'sel': 'pemilih_a916db4e', 'seconds': '초단위', 'log': 'LOG_baris', 'at': 'saat_ini_posisi', 'send': 'kirim', 'main': 'jalankan', 'req': 'permintaan_VALUE', 'hot': 'pintasan_VALUE', 'pump': 'handel_acara', 'ROOT': 'Tugas_akar', 'marker': '확인표시', 'b': 'SECOND_VALUE', 'command': 'perintah', 'shell': 'shell', 'f': 'file_entri', 'color': '색상', 'click': 'klik_tombol', 'k': '셋째순번', 'c': 'kode_karakter', 'r': '반환값', 'p': 'data_posisi', 'done': 'Selesai_jumlah', 'end': 'mengakhiri_OFFSET', 'command_mode': 'perintah_MODE', 'key': '누름값', 'y': 'Y_koordinat', 'pixels': '화소들', 'result': 'hasil', 'report': 'validasi_lapor', 'dest': 'tujuan_VALUE_posisi', 'work': '작업경로', 'qmp': '모의제어접속'}
    for 이전, saat_ini_item in 대응.items():
        if hasattr(implementasi, saat_ini_item): globals()[이전] = getattr(implementasi, saat_ini_item)
