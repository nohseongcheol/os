#!/usr/bin/env python3
"""기존 jalur 호환 entri_p. aktual_data implementasi: ../alat/desktop_Tampilan.py"""
import importlib as TAKE_VALUE
import sys as sistem_operasi_VALUE
from pathlib import Path as jalur
sistem_operasi_VALUE.path.insert(0, str(jalur(__file__).resolve().parents[1] / 'alat'))
if __name__ == '__main__':
    import runpy as apl_peluncur
    apl_peluncur.run_module('desktop_Tampilan', run_name='__main__', alter_sys=True)
else:
    implementasi = TAKE_VALUE.import_module('desktop_Tampilan')
    대응 = {'count': 'entri_COUNT', 'special': '특수글쇠', 'error': 'galat', 'exact': 'EXACT_VALUE', 'network': 'jaringan', 'closed': '닫힘', 'length': 'panjang_VALUE', 'opened': '열림', 'ftp_port': 'transfer_file_nomor_port', 'server': 'server_VALUE', 'resources': 'Referensi_50487cae', 'data': 'data', 'shift': 'tombol_SHIFT', 'send': 'kirim', 'run_desktop': 'eksekusi_desktop', 'protocol': '통신규약', 'forwards': '전달규칙들', 'host': 'host', 'text': 'teks', 'korean': '한글여부', 'port': 'nomor_port', 'signum': '신호번호', 'version': 'nomor_versi', 'parser': 'parser', 'bridge': 'bridge', 'kind': 'area_VALUE', 'tail': '끝부분', 'size': 'Ukuran', 'previous_buttons': '이전단추', 'key': '누름값', 'y': 'Y_koordinat', 'prefix': '앞부분', 'client': 'klien', 'char': 'data_karakter', 'work': '작업경로', 'Keyboard': 'keyboard', 'x': 'koordinat_x', 'down': '누르는중', 'net': 'jaringan_bridge_entri', 'self': '자신', 'mode_changed': '입력방식알림', 'serial': '직렬입출력', 'args': 'argumen_ARRAY', 'Hangul': '한글조합', 'chunk': '조각', 'proc': 'Proses', 'Desktop': 'CONNECT_desktop', 'buttons': '단추들', 'thread': 'tugasLatar', 'pressed': '눌림', 'previous': '이전항목', 'toggle': 'SWITCH_MODE', 'command': 'perintah', 'sock': '소켓', 'frame': '실행틀', 'ctrl': 'CTRL', 'path': 'jalur', 'cp': 'pengodean_karakter', 'terminate': '종료시키기', 'security': 'Keamanan', 'vnc_port': '원격화면접속번호', 'body': 'teks_isi', 'index': 'LOOKUP_INDEX', 'exited': '종료됨', 'keysym': 'Kunci_simbol', 'output': '출력결과', 'keyboard': 'keyboard_entri', 'interrupted': '가로채기됨', 'listener': 'terima_port', 'reader': 'Pembaca', 'NetworkBridge': 'jaringan_bridge', 'gui': '그림화면', 'worker': 'pemrosesan_tugas'}
    for 이전, saat_ini_item in 대응.items():
        if hasattr(implementasi, saat_ini_item): globals()[이전] = getattr(implementasi, saat_ini_item)
