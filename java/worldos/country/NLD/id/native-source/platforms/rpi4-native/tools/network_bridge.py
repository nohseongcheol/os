#!/usr/bin/env python3
"""기존 jalur 호환 entri_p. aktual_data implementasi: ../alat/jaringan_bridge.py"""
import importlib as TAKE_VALUE
import sys as sistem_operasi_VALUE
from pathlib import Path as jalur
sistem_operasi_VALUE.path.insert(0, str(jalur(__file__).resolve().parents[1] / 'alat'))
if __name__ == '__main__':
    import runpy as apl_peluncur
    apl_peluncur.run_module('jaringan_bridge', run_name='__main__', alter_sys=True)
else:
    implementasi = TAKE_VALUE.import_module('jaringan_bridge')
    대응 = {'response': 'respons', 'parts': 'jalur_komponen', 's': 'string_data', 'i': '순번', 'close': 'Tutup', 'forward': '전달규칙', 'slip_input': '직렬전문입력', 'self': '자신', 'item': 'entri_VALUE', 'flags': 'konfigurasi_Background_Intelligent_Transfer_Service', 'ftp_port': 'transfer_file_nomor_port', 'args': 'argumen_ARRAY', 'server': 'server_VALUE', 'data': 'data', 'ethernet_input': '이더넷입력', 'trace_packet': 'trace_paket', 'GATEWAY': '관문기계주소', 'rule': 'aturan_VALUE', 'protocol': '통신규약', 'forwards': '전달규칙들', 'occupied': '사용중주소', 'host': 'host', 'ack': '확인번호', 'serial_port': '직렬접속번호', 'readers': '읽기대상들', 'guest': 'tamu', 'destination': 'tujuan_data_surel', 'ethernet_port': 'port_Ethernet', 'b': 'SECOND_VALUE', 'MAC': 'mesin_surel', 'arp': 'surel_resolusi_paket', 'writable': 'bisa_tulis', 'direction': '방향', 'seq': '순서번호', 'frame': '실행틀', 'loop': 'Siklus_VALUE', 'port': 'nomor_port', 'offset': 'OFFSET_VALUE', 'readable': '읽을수있음', 'c': 'kode_karakter', 'p': 'data_posisi', 'writers': '쓰기대상들', 'IP': 'Alamat_internet_VALUE', 'e': '보조항목', 'n': 'item_COUNT', 'packet': 'paket_data', 'arguments': '전달인수', 'source': '원본자료', 'NetworkBridge': 'jaringan_bridge', 'window': 'Jendela', 'capture': 'ambil'}
    for 이전, saat_ini_item in 대응.items():
        if hasattr(implementasi, saat_ini_item): globals()[이전] = getattr(implementasi, saat_ini_item)
