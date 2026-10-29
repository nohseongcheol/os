#!/usr/bin/env python3
"""기존 jalur 호환 entri_p. aktual_data implementasi: ../alat/예제시험.py"""
import importlib as TAKE_VALUE
import sys as sistem_operasi_VALUE
from pathlib import Path as jalur
sistem_operasi_VALUE.path.insert(0, str(jalur(__file__).resolve().parents[1] / 'alat'))
if __name__ == '__main__':
    import runpy as apl_peluncur
    apl_peluncur.run_module('예제시험', run_name='__main__', alter_sys=True)
else:
    implementasi = TAKE_VALUE.import_module('예제시험')
    대응 = {'count': 'entri_COUNT', 'exact': 'EXACT_VALUE', 'expected_file': '예상파일', 'ftp_port': 'transfer_file_nomor_port', 'data': 'data', 'graphics_command': 'grafis_perintah', 'main': 'jalankan', 'row': 'ROW_posisi', 'init': '초기값', 'target': 'target', 'ROOT': 'Tugas_akar', 'text': 'teks', 'binary': 'biner', 'out': 'KR_data', 'entry': 'entri_p', 'got': 'RECEIVED_COUNT', 'port': 'nomor_port', 'graphics_start': 'Mulai_gambar', 'col': 'kolom_posisi', 'begin': 'Mulai_OFFSET', 'kind': 'area_VALUE', 'selector': 'pemilih', 'n': 'item_COUNT', 'key': '누름값', 'y': 'Y_koordinat', 'client': 'klien', 'line': 'baris_masukan', 'report': 'validasi_lapor', 'language': 'Bahasa', 'x': 'koordinat_x', 'start': 'jalankan', 'rgb': '빛삼원색', 'down': '누르는중', 'listing': 'kirim_Daftar', 'payload': 'payload_data', 'proc': 'Proses', 'w': '너비값', 'temporary': '임시자원', 'echo': 'echo_server_entri', 'label': 'nama_tabel', 'content': 'Isi_VALUE', 'argument': '전달값', 'EchoServers': 'echo_Server', 'marker': '확인표시', 'expected': '예상결과', 'test_language': 'test_언어', 'filename': 'file_entri_nama', 'shell': 'shell', 'color': '색상', 'transcript': 'transkrip', 'offset': 'OFFSET_VALUE', 'h': '높이값', 'run': 'Jalankan_perintah', 'c': 'kode_karakter', 'path': 'jalur', 'encoding': 'tataan_karakter', 'end': 'mengakhiri_OFFSET', 'ftp': 'transfer_file_koneksi', 'pixels': '화소들', 'symbol': 'simbol_VALUE', 'source': '원본자료', 'name': 'Nama_2', 'receive': 'terima_email', 'manifest': '꾸러미명세'}
    for 이전, saat_ini_item in 대응.items():
        if hasattr(implementasi, saat_ini_item): globals()[이전] = getattr(implementasi, saat_ini_item)
