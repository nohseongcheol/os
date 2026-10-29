#!/usr/bin/env python3
"""기존 Bide_izena 호환 sarrera_p. benetako_datuak 구현: ../Tresnak/예제되돌림서버.py"""
import importlib as HARTU_balio
import sys as sistema_eragile_balio
from pathlib import Path as Bide_izena
sistema_eragile_balio.path.insert(0, str(Bide_izena(__file__).resolve().parents[1] / 'Tresnak'))
if __name__ == '__main__':
    import runpy as aplik_abiarazle
    aplik_abiarazle.run_module('예제되돌림서버', run_name='__main__', alter_sys=True)
else:
    구현 = HARTU_balio.import_module('예제되돌림서버')
    대응 = {'data': 'datuak', 'sock': '소켓', 'tcp_port': 'TCP_ataka', 'chunk': '조각', 'received': '수신됨', 'self': '자신', 'UDP': '전문요청처리', 'thread': '작업가닥', 'echo': 'atzeko_planoko_eguneratze_zerbitzari_sarrera', 'TCP': 'helduleku_konexio_eskaera', 'EchoServers': 'atzeko_planoko_eguneratze_Zerbitzariak', 'parser': 'analizatzaile', 'server': 'zerbitzari_balio', 'udp_port': 'UDP_ataka', 'args': 'arg_matrize'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
