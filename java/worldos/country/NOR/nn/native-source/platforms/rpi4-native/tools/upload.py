#!/usr/bin/env python3
"""기존 STIGE 호환 oppføring_p. faktisk_data 구현: ../Verktøy/Upload_Filer.py"""
import importlib as TAKE_VALUE
import sys as operativsystem_VALUE
from pathlib import Path as STIGE
operativsystem_VALUE.path.insert(0, str(STIGE(__file__).resolve().parents[1] / 'Verktøy'))
if __name__ == '__main__':
    import runpy as app_appskuff
    app_appskuff.run_module('Upload_Filer', run_name='__main__', alter_sys=True)
else:
    구현 = TAKE_VALUE.import_module('Upload_Filer')
    대응 = {'data': 'data', 'i': '순번', 'name': 'Namn', 'c': 'teiknkode', 'p': 'data_plassere', 'args': 'argument_ARRAY'}
    for 이전, betalt_vare in 대응.items():
        if hasattr(구현, betalt_vare): globals()[이전] = getattr(구현, betalt_vare)
