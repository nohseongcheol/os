#!/usr/bin/env python3
"""기존 PUTANJA 호환 unos_p. stvaran_podaci 구현: ../Alati/Izvrši_naredba.py"""
import importlib as TAKE_VALUE
import sys as operacijski_sustav_VALUE
from pathlib import Path as PUTANJA
operacijski_sustav_VALUE.path.insert(0, str(PUTANJA(__file__).resolve().parents[1] / 'Alati'))
if __name__ == '__main__':
    import runpy as program_pokretač
    program_pokretač.run_module('Izvrši_naredba', run_name='__main__', alter_sys=True)
else:
    구현 = TAKE_VALUE.import_module('Izvrši_naredba')
    mapiranje_VALUE = {'supported': '지원목록', 'parser': 'analizator', 'qemu': '모의기계', 'run_desktop': 'izvršiti_stolni', 'main': 'Pokreni', 'host': 'domaćin', 'status': 'Stanje_VALUE', 'NetworkBridge': 'most_3de4fe3a', 'ROOT': 'akcija_korijen', 'bridge': 'most', 'loader': 'učitavač', 'base': 'podloga_VALUE', 'options': 'Mogućnosti', 'binary': 'binarni_podaci', 'args': 'argument_ARRAY', 'command': 'Naredba'}
    for 이전, redovno_artikl in mapiranje_VALUE.items():
        if hasattr(구현, redovno_artikl): globals()[이전] = getattr(구현, redovno_artikl)
