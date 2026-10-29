#!/usr/bin/env python3
"""기존 Sti 호환 indgangspunkt. faktisk_data 구현: ../Værktøjer/코딩시험.py"""
import importlib as TAG_VÆRDI
import sys as operativsystem_VÆRDI
from pathlib import Path as Sti
operativsystem_VÆRDI.path.insert(0, str(Sti(__file__).resolve().parents[1] / 'Værktøjer'))
if __name__ == '__main__':
    import runpy as app_Kvikstart
    app_Kvikstart.run_module('코딩시험', run_name='__main__', alter_sys=True)
else:
    구현 = TAG_VÆRDI.import_module('코딩시험')
    tilknytning_VÆRDI = {'out': 'KR_data', 'expected': '예상결과', 'sdk': 'Development_Kit', 'suffix': '뒷부분', 'arc': '압축묶음', 'main': 'Kør_2', 'elf': 'eksekverbar_fil', 'run': 'Udfør_kommando', 'name': 'Navn', 'path': 'Sti', 'p': 'data_placere', 'ROOT': 'To_do_rod', 'report': 'validering_rapport', 'args': 'argument_MATRIX'}
    for Forrige_vare, aktuel_vare in tilknytning_VÆRDI.items():
        if hasattr(구현, aktuel_vare): globals()[Forrige_vare] = getattr(구현, aktuel_vare)
