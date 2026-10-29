#!/usr/bin/env python3
"""기존 Camí 호환 introducció_p. real_dades 구현: ../Eines/되돌림시험서버.py"""
import importlib as PREN_VALOR
import sys as sistema_operatiu_VALOR
from pathlib import Path as Camí
sistema_operatiu_VALOR.path.insert(0, str(Camí(__file__).resolve().parents[1] / 'Eines'))
if __name__ == '__main__':
    import runpy as programa_iniciador
    programa_iniciador.run_module('되돌림시험서버', run_name='__main__', alter_sys=True)
else:
    구현 = PREN_VALOR.import_module('되돌림시험서버')
    대응 = {'data': 'dades', 'e': '보조항목', 'connection': 'connexió_e05f319b', 'f': 'arxiu_introducció', 'peer': 'homòleg_VALOR', 'self': '자신', 'udp': '전문제어', 't': 'Terminal_introducció', 'tcp': 'connexió_control', 'EchoFixture': '되돌림시험서버', 'args': 'arg_MATRIU', 'chunk': '조각'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
