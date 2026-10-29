#!/usr/bin/env python3
"""기존 LALUAN 호환 titik_permulaan. sebenar_data pelaksanaan: ../alat/예제시험.py"""
import importlib as TAKE_VALUE
import sys as sistem_pengendalian_VALUE
from pathlib import Path as LALUAN
sistem_pengendalian_VALUE.path.insert(0, str(LALUAN(__file__).resolve().parents[1] / 'alat'))
if __name__ == '__main__':
    import runpy as aplikasi_pelancar
    aplikasi_pelancar.run_module('예제시험', run_name='__main__', alter_sys=True)
else:
    pelaksanaan = TAKE_VALUE.import_module('예제시험')
    대응 = {'count': 'pemasukan_COUNT', 'exact': 'EXACT_VALUE', 'expected_file': '예상파일', 'ftp_port': 'pemindahan_fail_nombor_port', 'data': 'data', 'graphics_command': 'grafik_perintah', 'main': 'Jalan', 'row': 'ROW_jawatan', 'init': '초기값', 'target': 'sasaran', 'ROOT': 'projek_akar', 'text': 'Teks', 'binary': 'perduaan', 'out': 'ukuran_data', 'entry': 'titik_permulaan', 'got': 'RECEIVED_COUNT', 'port': 'nombor_port', 'graphics_start': 'Mula_lukisan', 'col': 'lajur_jawatan', 'begin': 'Mula_Ofset', 'kind': 'bidang_VALUE', 'selector': '준비선택기', 'n': 'item_COUNT', 'key': '누름값', 'y': 'Y_koordinat', 'client': 'klien', 'line': 'baris', 'report': 'pensahihan_lapor', 'language': 'Bahasa', 'x': 'koordinat_x', 'start': 'Jalan', 'rgb': '빛삼원색', 'down': '누르는중', 'listing': 'e_mel_Senarai', 'payload': 'muat_beban_data', 'proc': 'Proses', 'w': '너비값', 'temporary': '임시자원', 'echo': '되돌림서버항목', 'label': 'nama_jadual', 'content': 'Kandungan_VALUE', 'argument': '전달값', 'EchoServers': '되돌림서버', 'marker': 'penanda', 'expected': '예상결과', 'test_language': 'ujian_Bahasa', 'filename': 'fail_pemasukan_nama', 'shell': 'cangkerang', 'color': '색상', 'transcript': '대화기록', 'offset': 'Ofset_VALUE', 'h': '높이값', 'run': 'laksanakan_perintah', 'c': 'titik_kod', 'path': 'LALUAN', 'encoding': 'set_aksara', 'end': 'tamat_Ofset', 'ftp': 'pemindahan_fail_hubungan', 'pixels': '화소들', 'symbol': 'simbol_VALUE', 'source': '원본자료', 'name': 'Nama', 'receive': '수신하기', 'manifest': 'pakej_manifes_aplikasi'}
    for 이전, 현재 in 대응.items():
        if hasattr(pelaksanaan, 현재): globals()[이전] = getattr(pelaksanaan, 현재)
