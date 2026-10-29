#!/usr/bin/env python3
"""기존 Sti 호환 indgangspunkt. faktisk_data 구현: ../Værktøjer/Upload_Filer.py"""
import importlib as TAG_VÆRDI
import sys as operativsystem_VÆRDI
from pathlib import Path as Sti
operativsystem_VÆRDI.path.insert(0, str(Sti(__file__).resolve().parents[1] / 'Værktøjer'))
if __name__ == '__main__':
    import runpy as app_Kvikstart
    app_Kvikstart.run_module('Upload_Filer', run_name='__main__', alter_sys=True)
else:
    구현 = TAG_VÆRDI.import_module('Upload_Filer')
    tilknytning_VÆRDI = {'data': 'data', 'i': '순번', 'name': 'Navn', 'c': 'tegnkode', 'p': 'data_placere', 'args': 'argument_MATRIX'}
    for Forrige_vare, aktuel_vare in tilknytning_VÆRDI.items():
        if hasattr(구현, aktuel_vare): globals()[Forrige_vare] = getattr(구현, aktuel_vare)
