#!/usr/bin/env python3
"""기존 Camí 호환 introducció_p. real_dades 구현: ../Eines/Executa_ordre.py"""
import importlib as PREN_VALOR
import sys as sistema_operatiu_VALOR
from pathlib import Path as Camí
sistema_operatiu_VALOR.path.insert(0, str(Camí(__file__).resolve().parents[1] / 'Eines'))
if __name__ == '__main__':
    import runpy as programa_iniciador
    programa_iniciador.run_module('Executa_ordre', run_name='__main__', alter_sys=True)
else:
    구현 = PREN_VALOR.import_module('Executa_ordre')
    대응 = {'supported': '지원목록', 'parser': 'analitzador', 'qemu': '모의기계', 'run_desktop': 'execució_escriptori', 'main': 'Executa_2', 'host': 'allotjar', 'status': 'Estat_VALOR', 'NetworkBridge': 'xarxa_pont', 'ROOT': 'Project_rel', 'bridge': 'pont', 'loader': '적재기', 'base': 'Fons_VALOR', 'options': 'Opcions', 'binary': 'binari', 'args': 'arg_MATRIU', 'command': 'Ordre'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
