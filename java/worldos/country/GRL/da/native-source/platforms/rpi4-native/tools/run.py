#!/usr/bin/env python3
"""기존 Sti 호환 indgangspunkt. faktisk_data 구현: ../Værktøjer/Udfør_kommando.py"""
import importlib as TAG_VÆRDI
import sys as operativsystem_VÆRDI
from pathlib import Path as Sti
operativsystem_VÆRDI.path.insert(0, str(Sti(__file__).resolve().parents[1] / 'Værktøjer'))
if __name__ == '__main__':
    import runpy as app_Kvikstart
    app_Kvikstart.run_module('Udfør_kommando', run_name='__main__', alter_sys=True)
else:
    구현 = TAG_VÆRDI.import_module('Udfør_kommando')
    tilknytning_VÆRDI = {'supported': '지원목록', 'parser': 'parser', 'qemu': '모의기계', 'run_desktop': 'køre_desktop', 'main': 'Kør_2', 'host': 'vært', 'status': 'status_VÆRDI', 'NetworkBridge': 'bro_3de4fe3a', 'ROOT': 'To_do_rod', 'bridge': 'bro', 'loader': 'indlæsningsfunktion', 'base': 'Baggrund_VÆRDI', 'options': 'Indstillinger_7f769d16', 'binary': 'binær', 'args': 'argument_MATRIX', 'command': 'Kommando'}
    for Forrige_vare, aktuel_vare in tilknytning_VÆRDI.items():
        if hasattr(구현, aktuel_vare): globals()[Forrige_vare] = getattr(구현, aktuel_vare)
