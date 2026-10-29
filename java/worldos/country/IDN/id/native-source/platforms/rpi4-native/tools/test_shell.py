#!/usr/bin/env python3
"""기존 jalur 호환 entri_p. aktual_data implementasi: ../alat/셸시험.py"""
import importlib as TAKE_VALUE
import sys as sistem_operasi_VALUE
from pathlib import Path as jalur
sistem_operasi_VALUE.path.insert(0, str(jalur(__file__).resolve().parents[1] / 'alat'))
if __name__ == '__main__':
    import runpy as apl_peluncur
    apl_peluncur.run_module('셸시험', run_name='__main__', alter_sys=True)
else:
    implementasi = TAKE_VALUE.import_module('셸시험')
    대응 = {'timeout': '시간제한', 'x': 'koordinat_x', 'msg': 'jaringan_email', 'i': '순번', 'reply': 'balas', 'call': '호출', 'args': 'argumen_ARRAY', 'chunk': '조각', 'data': 'data', 'proc': 'Proses', 'long_text': '긴글', 'restored': '복원자료', 'send': 'kirim', 'file': 'berkas', 'main': 'jalankan', 'found': 'Cari_KR', 'ROOT': 'Tugas_akar', 'text': 'teks', 'marker': '확인표시', 'command': 'perintah', 'expected': '예상결과', 'pixel': 'elgam', 'shell': 'shell', 'poll': '준비살피미', 'transcript': 'transkrip', 'end': 'mengakhiri_OFFSET', 'image': 'foto', 'key': '누름값', 'y': 'Y_koordinat', 'output': '출력결과', 'result': 'hasil', 'client': 'klien', 'line': 'baris_masukan', 'stream': 'Stream_VALUE', 'name': 'Nama_2', 'value': 'VALUE', 'receive': 'terima_email', 'report': 'validasi_lapor', 'work': '작업경로', 'qmp': '모의제어접속'}
    for 이전, saat_ini_item in 대응.items():
        if hasattr(implementasi, saat_ini_item): globals()[이전] = getattr(implementasi, saat_ini_item)
