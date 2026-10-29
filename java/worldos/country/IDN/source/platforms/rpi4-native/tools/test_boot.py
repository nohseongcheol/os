#!/usr/bin/env python3
"""기존 jalur 호환 entri_p. aktual_data implementasi: ../alat/부팅시험.py"""
import importlib as TAKE_VALUE
import sys as sistem_operasi_VALUE
from pathlib import Path as jalur
sistem_operasi_VALUE.path.insert(0, str(jalur(__file__).resolve().parents[1] / 'alat'))
if __name__ == '__main__':
    import runpy as apl_peluncur
    apl_peluncur.run_module('부팅시험', run_name='__main__', alter_sys=True)
else:
    implementasi = TAKE_VALUE.import_module('부팅시험')
    대응 = {'timeout': '시간제한', 'response': 'respons', 'msg': 'jaringan_email', 'exact': 'EXACT_VALUE', 'markers': '확인표시들', 'i': '순번', 'match': '일치', 'execute': 'Eksekusi', 'cancel': 'Batal_bedah', 'cmd_byte': 'perintah_byte', 'reply': 'balas', 'points': '지점들', 'server': 'server_VALUE', 'data': 'data', 'prompt': 'minta', 'enter': 'masukkan', 'imported': '들여온파일', 'send': 'kirim', 'main': 'jalankan', 'ROOT': 'Tugas_akar', 'text': 'teks', 'first_gui': '첫화면', 'pixel': 'elgam', 'java_class': '자바클래스', 'upload': 'Upload_File', 'pixels_file': 'elgam_file', 'pixels_data': 'elgam_data', 'edit': 'Edit_VALUE', 'receive_until': '표시까지받기', 'selector': 'pemilih', 'size': 'Ukuran', 'qmp_path': '모의제어경로', 'key': '누름값', 'second_gui': 'SECOND_GUI', 'y': 'Y_koordinat', 'result': 'hasil', 'samples': '예제들', 'client': 'klien', 'line': 'baris_masukan', 'report': 'validasi_lapor', 'work': '작업경로', 'x': 'koordinat_x', 'python_checks': '파이썬검사', 'download': 'unduh', 'greeting': '인사', 'dims': '치수', 'chunk': '조각', 'deadline': 'tenggat_waktu_TIME', 'proc': 'Proses', 'content': 'Isi_VALUE', 'block': 'blok_data', 'marker': '확인표시', 'command': 'perintah', 'expected': '예상결과', 'shell': 'shell', 'drawing': 'gambar_jalur', 'f': 'file_entri', 'transcript': 'transkrip', 'offset': 'OFFSET_VALUE', 'path': 'jalur', 'screenshot': 'kliping_layar', 'arguments': '전달인수', 'pixels': '화소들', 'viewer': '화면접속자', 'output': '출력결과', 'stream': 'Stream_VALUE', 'cmd': '명령인수', 'name': 'Nama_2', 'qmp': '모의제어접속'}
    for 이전, saat_ini_item in 대응.items():
        if hasattr(implementasi, saat_ini_item): globals()[이전] = getattr(implementasi, saat_ini_item)
