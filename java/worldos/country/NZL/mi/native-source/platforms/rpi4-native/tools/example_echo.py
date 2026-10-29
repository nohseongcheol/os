#!/usr/bin/env python3
"""기존 ara 호환 tāurunga_ira. tūturu_raraunga 구현: ../Ngā_Utauta/예제되돌림서버.py"""
import importlib as TAKE_uara
import sys as pūnaha_mahi_uara
from pathlib import Path as ara
pūnaha_mahi_uara.path.insert(0, str(ara(__file__).resolve().parents[1] / 'Ngā_Utauta'))
if __name__ == '__main__':
    import runpy as kaupapa_pūwhiri_taupānga
    kaupapa_pūwhiri_taupānga.run_module('예제되돌림서버', run_name='__main__', alter_sys=True)
else:
    구현 = TAKE_uara.import_module('예제되돌림서버')
    대응 = {'data': 'raraunga', 'sock': '소켓', 'tcp_port': 'TCP_kawe', 'chunk': '조각', 'received': '수신됨', 'self': '자신', 'UDP': '전문요청처리', 'thread': '작업가닥', 'echo': '되돌림서버항목', 'TCP': '연결요청처리', 'EchoServers': '되돌림서버', 'parser': '인수해석기', 'server': 'tūmau_uara', 'udp_port': 'UDP_kawe', 'args': 'tohenga_HUĀNGA'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
