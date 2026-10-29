#!/usr/bin/env python3
"""기존 Putanja 호환 unos_p. stvaran_podaci 구현: ../Alati/Upload_Fajlovi.py"""
import importlib as TAKE_VALUE
import sys as operativni_sistem_VALUE
from pathlib import Path as Putanja
operativni_sistem_VALUE.path.insert(0, str(Putanja(__file__).resolve().parents[1] / 'Alati'))
if __name__ == '__main__':
    import runpy as program_pokretač
    program_pokretač.run_module('Upload_Fajlovi', run_name='__main__', alter_sys=True)
else:
    구현 = TAKE_VALUE.import_module('Upload_Fajlovi')
    대응 = {'data': 'podaci', 'i': '순번', 'name': 'Naziv', 'c': 'kôd_znaka', 'p': 'podaci_položaj', 'args': 'argument_niz'}
    for 이전, trenutno_stavka in 대응.items():
        if hasattr(구현, trenutno_stavka): globals()[이전] = getattr(구현, trenutno_stavka)
