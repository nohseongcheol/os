#!/usr/bin/env python3
"""기존 LALUAN 호환 titik_permulaan. sebenar_data pelaksanaan: ../alat/rangkaian_penghubung.py"""
import importlib as TAKE_VALUE
import sys as sistem_pengendalian_VALUE
from pathlib import Path as LALUAN
sistem_pengendalian_VALUE.path.insert(0, str(LALUAN(__file__).resolve().parents[1] / 'alat'))
if __name__ == '__main__':
    import runpy as aplikasi_pelancar
    aplikasi_pelancar.run_module('rangkaian_penghubung', run_name='__main__', alter_sys=True)
else:
    pelaksanaan = TAKE_VALUE.import_module('rangkaian_penghubung')
    대응 = {'response': 'respons', 'parts': 'laluan_komponen', 's': 'rentetan_data', 'i': '순번', 'close': 'Tutup', 'forward': '전달규칙', 'slip_input': '직렬전문입력', 'self': '자신', 'item': 'pemasukan_VALUE', 'flags': 'konfigurasi_Background_Intelligent_Transfer_Service', 'ftp_port': 'pemindahan_fail_nombor_port', 'args': 'argumen_ARRAY', 'server': 'pelayan_VALUE', 'data': 'data', 'ethernet_input': '이더넷입력', 'trace_packet': 'jejak_paket', 'GATEWAY': '관문기계주소', 'rule': 'penapis_VALUE', 'protocol': '통신규약', 'forwards': '전달규칙들', 'occupied': '사용중주소', 'host': 'hos', 'ack': '확인번호', 'serial_port': '직렬접속번호', 'readers': '읽기대상들', 'guest': 'tetamu', 'destination': 'destinasi_data_e_mel', 'ethernet_port': 'port_Ethernet', 'b': 'SECOND_VALUE', 'MAC': 'mesin_e_mel', 'arp': 'e_mel_resolusi_paket', 'writable': '쓸수있음', 'direction': '방향', 'seq': '순서번호', 'frame': '실행틀', 'loop': 'Kitaran_VALUE', 'port': 'nombor_port', 'offset': 'Ofset_VALUE', 'readable': '읽을수있음', 'c': 'titik_kod', 'p': 'data_jawatan', 'writers': '쓰기대상들', 'IP': 'alamat_Internet_VALUE', 'e': '보조항목', 'n': 'item_COUNT', 'packet': 'paket_data', 'arguments': '전달인수', 'source': '원본자료', 'NetworkBridge': 'rangkaian_penghubung', 'window': 'Tetingkap', 'capture': 'rakam'}
    for 이전, 현재 in 대응.items():
        if hasattr(pelaksanaan, 현재): globals()[이전] = getattr(pelaksanaan, 현재)
