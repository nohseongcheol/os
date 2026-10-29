#!/usr/bin/env python3
"""기존 Sti 호환 indgangspunkt. faktisk_data 구현: ../Værktøjer/test_strøm.py"""
import importlib as TAG_VÆRDI
import sys as operativsystem_VÆRDI
from pathlib import Path as Sti
operativsystem_VÆRDI.path.insert(0, str(Sti(__file__).resolve().parents[1] / 'Værktøjer'))
if __name__ == '__main__':
    import runpy as app_Kvikstart
    app_Kvikstart.run_module('test_strøm', run_name='__main__', alter_sys=True)
else:
    구현 = TAG_VÆRDI.import_module('test_strøm')
    tilknytning_VÆRDI = {'out': 'KR_data', 'main': 'Kør_2', 'ROOT': 'To_do_rod', 'p': 'data_placere', 'text': 'Tekst', 'report': 'validering_rapport'}
    for Forrige_vare, aktuel_vare in tilknytning_VÆRDI.items():
        if hasattr(구현, aktuel_vare): globals()[Forrige_vare] = getattr(구현, aktuel_vare)
