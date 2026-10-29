#!/usr/bin/env python3
"""기존 putanja 호환 stavka_p. stvarni_podaci 구현: ../Alatke/Izvrši_komanda.py"""
import importlib as TAKE_VALUE
import sys as operativni_sistem_VALUE
from pathlib import Path as putanja
operativni_sistem_VALUE.path.insert(0, str(putanja(__file__).resolve().parents[1] / 'Alatke'))
if __name__ == '__main__':
    import runpy as program_pokretač
    program_pokretač.run_module('Izvrši_komanda', run_name='__main__', alter_sys=True)
else:
    구현 = TAKE_VALUE.import_module('Izvrši_komanda')
    mapiranje_VALUE = {'supported': '지원목록', 'parser': 'analizator', 'qemu': '모의기계', 'run_desktop': 'koristiti_desktop', 'main': 'koristiti', 'host': 'host', 'status': 'Status_VALUE', 'NetworkBridge': 'mrežni_most', 'ROOT': 'radnja_koren', 'bridge': 'most', 'loader': 'rutina_za_punjenje', 'base': 'poster_VALUE', 'options': 'Opcije', 'binary': 'binarni', 'args': 'argument_niz', 'command': 'komanda'}
    for 이전, aktuelno_stavka in mapiranje_VALUE.items():
        if hasattr(구현, aktuelno_stavka): globals()[이전] = getattr(구현, aktuelno_stavka)
