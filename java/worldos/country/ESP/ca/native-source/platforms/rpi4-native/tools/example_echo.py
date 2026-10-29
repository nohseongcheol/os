#!/usr/bin/env python3
"""기존 Camí 호환 introducció_p. real_dades 구현: ../Eines/예제되돌림서버.py"""
import importlib as PREN_VALOR
import sys as sistema_operatiu_VALOR
from pathlib import Path as Camí
sistema_operatiu_VALOR.path.insert(0, str(Camí(__file__).resolve().parents[1] / 'Eines'))
if __name__ == '__main__':
    import runpy as programa_iniciador
    programa_iniciador.run_module('예제되돌림서버', run_name='__main__', alter_sys=True)
else:
    구현 = PREN_VALOR.import_module('예제되돌림서버')
    대응 = {'data': 'dades', 'sock': '소켓', 'tcp_port': 'TCP_port', 'chunk': '조각', 'received': '수신됨', 'self': '자신', 'UDP': '전문요청처리', 'thread': '작업가닥', 'echo': 'eco_servidor_introducció', 'TCP': 'control_connexió_sol_licitud', 'EchoServers': 'eco_Servidors', 'parser': 'analitzador', 'server': 'servidor_VALOR', 'udp_port': 'UDP_port', 'args': 'arg_MATRIU'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
