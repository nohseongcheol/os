#!/usr/bin/env python3
"""기존 Sti 호환 inngangspunkt. faktisk_data 구현: ../Verktøy/Upload_Filer.py"""
import importlib as TA_VERDI
import sys as operativsystem_VERDI
from pathlib import Path as Sti
operativsystem_VERDI.path.insert(0, str(Sti(__file__).resolve().parents[1] / 'Verktøy'))
if __name__ == '__main__':
    import runpy as app_appskuff
    app_appskuff.run_module('Upload_Filer', run_name='__main__', alter_sys=True)
else:
    구현 = TA_VERDI.import_module('Upload_Filer')
    tildeling_VERDI = {'data': 'data', 'i': '순번', 'name': 'Navn', 'c': 'tegnkode', 'p': 'data_plassere', 'args': 'argument_MATRISE'}
    for Forrige_vare, betalt_vare in tildeling_VERDI.items():
        if hasattr(구현, betalt_vare): globals()[Forrige_vare] = getattr(구현, betalt_vare)
