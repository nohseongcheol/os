#!/usr/bin/env python3
"""기존 jalur 호환 entri_p. aktual_data implementasi: ../alat/파일전송시험.py"""
import importlib as TAKE_VALUE
import sys as sistem_operasi_VALUE
from pathlib import Path as jalur
sistem_operasi_VALUE.path.insert(0, str(jalur(__file__).resolve().parents[1] / 'alat'))
if __name__ == '__main__':
    import runpy as apl_peluncur
    apl_peluncur.run_module('파일전송시험', run_name='__main__', alter_sys=True)
else:
    implementasi = TAKE_VALUE.import_module('파일전송시험')
    대응 = {'timeout': '시간제한', 'payload': 'payload_data', 'broken': '손상자료', 'linux_example': '리눅스예제', 'chunk': '조각', 'data': 'data', 'proc': 'Proses', 'code': 'instruksi_urutan', 'linux': '리눅스파일', 'archive': 'Arsip', 'main': 'jalankan', 'net_source': '통신원문', 'temporary': '임시자원', 'static_source': 'statik_sumber', 'java_source': '자바원문', 'echo': 'echo_server_entri', 'ROOT': 'Tugas_akar', 'text': 'teks', 'marker': '확인표시', 'EchoFixture': '되돌림시험서버', 'command': 'perintah', 'out': 'KR_data', 'expected': '예상결과', 'server_source': 'server_sumber', 'shell': 'shell', 'upload': 'Upload_File', 'transcript': 'transkrip', 'port': 'nomor_port', 'native': '자체실행파일', 'elf': '실행파일', 'server_udp_port': '서버전문접속번호', 'packed': '묶인자료', 'bridge': 'bridge', 'selector': 'pemilih', 'end': 'mengakhiri_OFFSET', 'e': '보조항목', 'ftp': 'transfer_file_koneksi', 'key': '누름값', 'bytecode': '바이트코드', 'peer': 'serekan_VALUE', 'result': 'hasil', 'unchanged': '보존자료', 'line': 'baris_masukan', 'server_tcp_port': 'server_Stream_port', 'source': '원본자료', 'NetworkBridge': 'jaringan_bridge', 'jar': '자바꾸러미', 'receive': 'terima_email', 'report': 'validasi_lapor'}
    for 이전, saat_ini_item in 대응.items():
        if hasattr(implementasi, saat_ini_item): globals()[이전] = getattr(implementasi, saat_ini_item)
