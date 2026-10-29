#!/usr/bin/env python3
"""기존 LALUAN 호환 titik_permulaan. sebenar_data pelaksanaan: ../alat/ujian_cangkerang.py"""
import importlib as TAKE_VALUE
import sys as sistem_pengendalian_VALUE
from pathlib import Path as LALUAN
sistem_pengendalian_VALUE.path.insert(0, str(LALUAN(__file__).resolve().parents[1] / 'alat'))
if __name__ == '__main__':
    import runpy as aplikasi_pelancar
    aplikasi_pelancar.run_module('ujian_cangkerang', run_name='__main__', alter_sys=True)
else:
    pelaksanaan = TAKE_VALUE.import_module('ujian_cangkerang')
    대응 = {'timeout': '시간제한', 'x': 'koordinat_x', 'msg': 'rangkaian_e_mel', 'i': '순번', 'reply': 'balas', 'call': '호출', 'args': 'argumen_ARRAY', 'chunk': '조각', 'data': 'data', 'proc': 'Proses', 'long_text': '긴글', 'restored': '복원자료', 'send': 'e_mel_9aee63bd', 'file': 'Fail', 'main': 'Jalan', 'found': 'Cari_ukuran', 'ROOT': 'projek_akar', 'text': 'Teks', 'marker': 'penanda', 'command': 'Perintah', 'expected': '예상결과', 'pixel': 'pel', 'shell': 'cangkerang', 'poll': '준비살피미', 'transcript': '대화기록', 'end': 'tamat_Ofset', 'image': 'imej', 'key': '누름값', 'y': 'Y_koordinat', 'output': '출력결과', 'result': 'ukuran', 'client': 'klien', 'line': 'baris', 'stream': 'strim_VALUE', 'name': 'Nama', 'value': 'VALUE', 'receive': '수신하기', 'report': 'pensahihan_lapor', 'work': '작업경로', 'qmp': '모의제어접속'}
    for 이전, 현재 in 대응.items():
        if hasattr(pelaksanaan, 현재): globals()[이전] = getattr(pelaksanaan, 현재)
