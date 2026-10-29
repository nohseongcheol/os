#!/usr/bin/env python3
"""기존 LALUAN 호환 titik_permulaan. sebenar_data pelaksanaan: ../alat/예제되돌림서버.py"""
import importlib as TAKE_VALUE
import sys as sistem_pengendalian_VALUE
from pathlib import Path as LALUAN
sistem_pengendalian_VALUE.path.insert(0, str(LALUAN(__file__).resolve().parents[1] / 'alat'))
if __name__ == '__main__':
    import runpy as aplikasi_pelancar
    aplikasi_pelancar.run_module('예제되돌림서버', run_name='__main__', alter_sys=True)
else:
    pelaksanaan = TAKE_VALUE.import_module('예제되돌림서버')
    대응 = {'data': 'data', 'sock': '소켓', 'tcp_port': 'TCP_port', 'chunk': '조각', 'received': '수신됨', 'self': '자신', 'UDP': '전문요청처리', 'thread': '작업가닥', 'echo': '되돌림서버항목', 'TCP': 'pemegang_hubungan_permintaan', 'EchoServers': '되돌림서버', 'parser': 'penghurai', 'server': 'pelayan_VALUE', 'udp_port': 'UDP_port', 'args': 'argumen_ARRAY'}
    for 이전, 현재 in 대응.items():
        if hasattr(pelaksanaan, 현재): globals()[이전] = getattr(pelaksanaan, 현재)
