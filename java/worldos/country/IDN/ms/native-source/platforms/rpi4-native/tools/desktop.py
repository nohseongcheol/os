#!/usr/bin/env python3
"""기존 LALUAN 호환 titik_permulaan. sebenar_data pelaksanaan: ../alat/meja_lihat.py"""
import importlib as TAKE_VALUE
import sys as sistem_pengendalian_VALUE
from pathlib import Path as LALUAN
sistem_pengendalian_VALUE.path.insert(0, str(LALUAN(__file__).resolve().parents[1] / 'alat'))
if __name__ == '__main__':
    import runpy as aplikasi_pelancar
    aplikasi_pelancar.run_module('meja_lihat', run_name='__main__', alter_sys=True)
else:
    pelaksanaan = TAKE_VALUE.import_module('meja_lihat')
    대응 = {'count': 'pemasukan_COUNT', 'special': '특수글쇠', 'error': 'RALAT', 'exact': 'EXACT_VALUE', 'network': 'rangkaian', 'closed': '닫힘', 'length': 'kepanjangan_VALUE', 'opened': '열림', 'ftp_port': 'pemindahan_fail_nombor_port', 'server': 'pelayan_VALUE', 'resources': 'Sumber', 'data': 'data', 'shift': 'kekunci_SHIFT', 'send': 'e_mel_9aee63bd', 'run_desktop': 'jalankan_meja', 'protocol': '통신규약', 'forwards': '전달규칙들', 'host': 'hos', 'text': 'Teks', 'korean': '한글여부', 'port': 'nombor_port', 'signum': '신호번호', 'version': 'nombor_versi', 'parser': 'penghurai', 'bridge': 'penghubung', 'kind': 'bidang_VALUE', 'tail': '끝부분', 'size': 'Saiz', 'previous_buttons': '이전단추', 'key': '누름값', 'y': 'Y_koordinat', 'prefix': '앞부분', 'client': 'klien', 'char': 'data_aksara', 'work': '작업경로', 'Keyboard': 'papan_kekunci', 'x': 'koordinat_x', 'down': '누르는중', 'net': 'rangkaian_penghubung_pemasukan', 'self': '자신', 'mode_changed': '입력방식알림', 'serial': '직렬입출력', 'args': 'argumen_ARRAY', 'Hangul': '한글조합', 'chunk': '조각', 'proc': 'Proses', 'Desktop': 'CONNECT_meja', 'buttons': '단추들', 'thread': '작업가닥', 'pressed': '눌림', 'previous': '이전항목', 'toggle': 'tukar_mod', 'command': 'Perintah', 'sock': '소켓', 'frame': '실행틀', 'ctrl': 'CTRL', 'path': 'LALUAN', 'cp': 'pengekodan_aksara', 'terminate': 'batal', 'security': 'Keselamatan', 'vnc_port': '원격화면접속번호', 'body': 'teks_jasad', 'index': 'Carian_INDEX', 'exited': '종료됨', 'keysym': 'Kunci_simbol', 'output': '출력결과', 'keyboard': 'papan_kekunci_pemasukan', 'interrupted': '가로채기됨', 'listener': '수신창구', 'reader': 'Pembaca', 'NetworkBridge': 'rangkaian_penghubung', 'gui': '그림화면', 'worker': 'pemprosesan_tugas'}
    for 이전, 현재 in 대응.items():
        if hasattr(pelaksanaan, 현재): globals()[이전] = getattr(pelaksanaan, 현재)
