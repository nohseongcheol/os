#!/usr/bin/env python3
"""기존 Camí 호환 introducció_p. real_dades 구현: ../Eines/pujar_Fitxers.py"""
import importlib as PREN_VALOR
import sys as sistema_operatiu_VALOR
from pathlib import Path as Camí
sistema_operatiu_VALOR.path.insert(0, str(Camí(__file__).resolve().parents[1] / 'Eines'))
if __name__ == '__main__':
    import runpy as programa_iniciador
    programa_iniciador.run_module('pujar_Fitxers', run_name='__main__', alter_sys=True)
else:
    구현 = PREN_VALOR.import_module('pujar_Fitxers')
    대응 = {'data': 'dades', 'i': '순번', 'name': 'Nom', 'c': 'codi_de_caràcter', 'p': 'dades_càrrec', 'args': 'arg_MATRIU'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
