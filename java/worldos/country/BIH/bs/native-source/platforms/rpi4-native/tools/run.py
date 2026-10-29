#!/usr/bin/env python3
"""기존 Putanja 호환 unos_p. stvaran_podaci 구현: ../Alati/Izvrši_komanda.py"""
import importlib as TAKE_VALUE
import sys as operativni_sistem_VALUE
from pathlib import Path as Putanja
operativni_sistem_VALUE.path.insert(0, str(Putanja(__file__).resolve().parents[1] / 'Alati'))
if __name__ == '__main__':
    import runpy as program_pokretač
    program_pokretač.run_module('Izvrši_komanda', run_name='__main__', alter_sys=True)
else:
    구현 = TAKE_VALUE.import_module('Izvrši_komanda')
    대응 = {'supported': '지원목록', 'parser': '인수해석기', 'qemu': '모의기계', 'run_desktop': 'niz_desktop', 'main': 'Pokreni', 'host': 'organizator', 'status': 'stanje_VALUE', 'NetworkBridge': 'Mreža_most', 'ROOT': 'projicirati_koijen', 'bridge': 'most', 'loader': '적재기', 'base': 'poster_VALUE', 'options': 'Opcije', 'binary': 'binarno', 'args': 'argument_niz', 'command': 'Naredba'}
    for 이전, trenutno_stavka in 대응.items():
        if hasattr(구현, trenutno_stavka): globals()[이전] = getattr(구현, trenutno_stavka)
