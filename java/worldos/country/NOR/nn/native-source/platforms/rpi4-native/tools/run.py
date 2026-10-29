#!/usr/bin/env python3
"""기존 STIGE 호환 oppføring_p. faktisk_data 구현: ../Verktøy/Utfør_kommando.py"""
import importlib as TAKE_VALUE
import sys as operativsystem_VALUE
from pathlib import Path as STIGE
operativsystem_VALUE.path.insert(0, str(STIGE(__file__).resolve().parents[1] / 'Verktøy'))
if __name__ == '__main__':
    import runpy as app_appskuff
    app_appskuff.run_module('Utfør_kommando', run_name='__main__', alter_sys=True)
else:
    구현 = TAKE_VALUE.import_module('Utfør_kommando')
    대응 = {'supported': '지원목록', 'parser': '인수해석기', 'qemu': '모의기계', 'run_desktop': 'køyre_stasjonær', 'main': 'Køyr_2', 'host': 'vert', 'status': 'status_VALUE', 'NetworkBridge': 'Nettverk_bru', 'ROOT': 'spegle_rot', 'bridge': 'bru', 'loader': '적재기', 'base': 'bakgrunn_VALUE', 'options': 'Alternativ', 'binary': 'binær', 'args': 'argument_ARRAY', 'command': 'Kommando'}
    for 이전, betalt_vare in 대응.items():
        if hasattr(구현, betalt_vare): globals()[이전] = getattr(구현, betalt_vare)
