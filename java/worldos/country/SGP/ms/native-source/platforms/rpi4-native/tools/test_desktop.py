#!/usr/bin/env python3
"""기존 LALUAN 호환 titik_permulaan. sebenar_data pelaksanaan: ../alat/ujian_meja.py"""
import importlib as TAKE_VALUE
import sys as sistem_pengendalian_VALUE
from pathlib import Path as LALUAN
sistem_pengendalian_VALUE.path.insert(0, str(LALUAN(__file__).resolve().parents[1] / 'alat'))
if __name__ == '__main__':
    import runpy as aplikasi_pelancar
    aplikasi_pelancar.run_module('ujian_meja', run_name='__main__', alter_sys=True)
else:
    pelaksanaan = TAKE_VALUE.import_module('ujian_meja')
    대응 = {'x': 'koordinat_x', 'typing': '글자입력', 'message': '알림문', 'start': 'Jalan', 'down': '누르는중', 'exact': 'EXACT_VALUE', 'i': '순번', 'press': 'tekan_Kunci', 'rectangles': '사각형들', 'sym': 'simbol', 'j': '안쪽순번', 'deadline': '마감시각', 'proc': 'Proses', 'data': 'data', 'main': 'Jalan', 'w': '너비값', 'init': '초기값', 'block': 'blok_data', 'ROOT': 'projek_akar', 'text': 'Teks', 'marker': 'penanda', 'report': 'pensahihan_lapor', 'until': '까지', 'clipboard': 'papan_klip_VALUE', 'dst': 'destinasi_e_mel', 'seen': '본항목들', 'poll': '준비살피미', 'transcript': '대화기록', 'port': 'nombor_port', 'offset': 'Ofset_VALUE', 'h': '높이값', 'src': '원본주소', 'event': 'Peristiwa', 'encoding': 'set_aksara', 'size': 'Saiz', 'key': '누름값', 'pixels': '화소들', 'y': 'Y_koordinat', 'output': '출력결과', 'symbol': 'simbol_VALUE', 'client': 'klien', 'char': 'data_aksara', 'rgb': '빛삼원색'}
    for 이전, 현재 in 대응.items():
        if hasattr(pelaksanaan, 현재): globals()[이전] = getattr(pelaksanaan, 현재)
