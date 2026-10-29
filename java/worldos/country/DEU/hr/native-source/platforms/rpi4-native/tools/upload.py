#!/usr/bin/env python3
"""기존 PUTANJA 호환 unos_p. stvaran_podaci 구현: ../Alati/Prijenos_Datoteke.py"""
import importlib as TAKE_VALUE
import sys as operacijski_sustav_VALUE
from pathlib import Path as PUTANJA
operacijski_sustav_VALUE.path.insert(0, str(PUTANJA(__file__).resolve().parents[1] / 'Alati'))
if __name__ == '__main__':
    import runpy as program_pokretač
    program_pokretač.run_module('Prijenos_Datoteke', run_name='__main__', alter_sys=True)
else:
    구현 = TAKE_VALUE.import_module('Prijenos_Datoteke')
    mapiranje_VALUE = {'data': 'podaci', 'i': '순번', 'name': 'Ime', 'c': 'kodna_točka', 'p': 'podaci_položaj', 'args': 'argument_ARRAY'}
    for 이전, redovno_artikl in mapiranje_VALUE.items():
        if hasattr(구현, redovno_artikl): globals()[이전] = getattr(구현, redovno_artikl)
