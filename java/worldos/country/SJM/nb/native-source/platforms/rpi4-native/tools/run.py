#!/usr/bin/env python3
"""기존 Sti 호환 inngangspunkt. faktisk_data 구현: ../Verktøy/Utfør_kommando.py"""
import importlib as TA_VERDI
import sys as operativsystem_VERDI
from pathlib import Path as Sti
operativsystem_VERDI.path.insert(0, str(Sti(__file__).resolve().parents[1] / 'Verktøy'))
if __name__ == '__main__':
    import runpy as app_appskuff
    app_appskuff.run_module('Utfør_kommando', run_name='__main__', alter_sys=True)
else:
    구현 = TA_VERDI.import_module('Utfør_kommando')
    tildeling_VERDI = {'supported': '지원목록', 'parser': 'parser', 'qemu': '모의기계', 'run_desktop': 'kjøre_stasjonær', 'main': 'Kjør_2', 'host': 'vert', 'status': 'status_VERDI', 'NetworkBridge': 'bro_3de4fe3a', 'ROOT': 'speile_rot', 'bridge': 'bro', 'loader': 'laster', 'base': 'bakgrunn_VERDI', 'options': 'Alternativer', 'binary': 'binær', 'args': 'argument_MATRISE', 'command': 'Kommando'}
    for Forrige_vare, betalt_vare in tildeling_VERDI.items():
        if hasattr(구현, betalt_vare): globals()[Forrige_vare] = getattr(구현, betalt_vare)
