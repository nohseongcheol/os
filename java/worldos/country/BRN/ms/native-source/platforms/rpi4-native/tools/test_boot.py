#!/usr/bin/env python3
"""기존 LALUAN 호환 titik_permulaan. sebenar_data pelaksanaan: ../alat/부팅시험.py"""
import importlib as TAKE_VALUE
import sys as sistem_pengendalian_VALUE
from pathlib import Path as LALUAN
sistem_pengendalian_VALUE.path.insert(0, str(LALUAN(__file__).resolve().parents[1] / 'alat'))
if __name__ == '__main__':
    import runpy as aplikasi_pelancar
    aplikasi_pelancar.run_module('부팅시험', run_name='__main__', alter_sys=True)
else:
    pelaksanaan = TAKE_VALUE.import_module('부팅시험')
    대응 = {'timeout': '시간제한', 'response': 'respons', 'msg': 'rangkaian_e_mel', 'exact': 'EXACT_VALUE', 'markers': '확인표시들', 'i': '순번', 'match': '일치', 'execute': 'Lakukan', 'cancel': 'Batal_operasi', 'cmd_byte': 'perintah_bait', 'reply': 'balas', 'points': '지점들', 'server': 'pelayan_VALUE', 'data': 'data', 'prompt': 'prom', 'enter': 'masuk', 'imported': '들여온파일', 'send': 'e_mel_9aee63bd', 'main': 'Jalan', 'ROOT': 'projek_akar', 'text': 'Teks', 'first_gui': '첫화면', 'pixel': 'pel', 'java_class': '자바클래스', 'upload': 'Upload_Fail', 'pixels_file': 'pel_fail', 'pixels_data': 'pel_data', 'edit': 'edit_VALUE', 'receive_until': '표시까지받기', 'selector': '준비선택기', 'size': 'Saiz', 'qmp_path': '모의제어경로', 'key': '누름값', 'second_gui': 'SECOND_GUI', 'y': 'Y_koordinat', 'result': 'ukuran', 'samples': '예제들', 'client': 'klien', 'line': 'baris', 'report': 'pensahihan_lapor', 'work': '작업경로', 'x': 'koordinat_x', 'python_checks': '파이썬검사', 'download': 'muat_turun', 'greeting': '인사', 'dims': '치수', 'chunk': '조각', 'deadline': '마감시각', 'proc': 'Proses', 'content': 'Kandungan_VALUE', 'block': 'blok_data', 'marker': 'penanda', 'command': 'Perintah', 'expected': '예상결과', 'shell': 'cangkerang', 'drawing': 'lukisan_laluan', 'f': 'fail_pemasukan', 'transcript': '대화기록', 'offset': 'Ofset_VALUE', 'path': 'LALUAN', 'screenshot': 'syot_layar', 'arguments': '전달인수', 'pixels': '화소들', 'viewer': '화면접속자', 'output': '출력결과', 'stream': 'strim_VALUE', 'cmd': '명령인수', 'name': 'Nama', 'qmp': '모의제어접속'}
    for 이전, 현재 in 대응.items():
        if hasattr(pelaksanaan, 현재): globals()[이전] = getattr(pelaksanaan, 현재)
