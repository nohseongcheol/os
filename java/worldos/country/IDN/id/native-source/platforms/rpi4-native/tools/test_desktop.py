#!/usr/bin/env python3
"""기존 jalur 호환 entri_p. aktual_data implementasi: ../alat/바탕화면시험.py"""
import importlib as TAKE_VALUE
import sys as sistem_operasi_VALUE
from pathlib import Path as jalur
sistem_operasi_VALUE.path.insert(0, str(jalur(__file__).resolve().parents[1] / 'alat'))
if __name__ == '__main__':
    import runpy as apl_peluncur
    apl_peluncur.run_module('바탕화면시험', run_name='__main__', alter_sys=True)
else:
    implementasi = TAKE_VALUE.import_module('바탕화면시험')
    대응 = {'x': 'koordinat_x', 'typing': '글자입력', 'message': '알림문', 'start': 'jalankan', 'down': '누르는중', 'exact': 'EXACT_VALUE', 'i': '순번', 'press': 'tekan_Kunci', 'rectangles': '사각형들', 'sym': 'simbol', 'j': '안쪽순번', 'deadline': 'tenggat_waktu_TIME', 'proc': 'Proses', 'data': 'data', 'main': 'jalankan', 'w': '너비값', 'init': '초기값', 'block': 'blok_data', 'ROOT': 'Tugas_akar', 'text': 'teks', 'marker': '확인표시', 'report': 'validasi_lapor', 'until': '까지', 'clipboard': 'clipboard_VALUE', 'dst': 'tujuan_surel', 'seen': '본항목들', 'poll': '준비살피미', 'transcript': 'transkrip', 'port': 'nomor_port', 'offset': 'OFFSET_VALUE', 'h': '높이값', 'src': '원본주소', 'event': 'Even', 'encoding': 'tataan_karakter', 'size': 'Ukuran', 'key': '누름값', 'pixels': '화소들', 'y': 'Y_koordinat', 'output': '출력결과', 'symbol': 'simbol_VALUE', 'client': 'klien', 'char': 'data_karakter', 'rgb': '빛삼원색'}
    for 이전, saat_ini_item in 대응.items():
        if hasattr(implementasi, saat_ini_item): globals()[이전] = getattr(implementasi, saat_ini_item)
