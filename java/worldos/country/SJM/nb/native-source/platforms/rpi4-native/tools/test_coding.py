#!/usr/bin/env python3
"""기존 Sti 호환 inngangspunkt. faktisk_data 구현: ../Verktøy/코딩시험.py"""
import importlib as TA_VERDI
import sys as operativsystem_VERDI
from pathlib import Path as Sti
operativsystem_VERDI.path.insert(0, str(Sti(__file__).resolve().parents[1] / 'Verktøy'))
if __name__ == '__main__':
    import runpy as app_appskuff
    app_appskuff.run_module('코딩시험', run_name='__main__', alter_sys=True)
else:
    구현 = TA_VERDI.import_module('코딩시험')
    tildeling_VERDI = {'out': 'KR_data', 'expected': '예상결과', 'sdk': 'utviklingspakke', 'suffix': '뒷부분', 'arc': '압축묶음', 'main': 'Kjør_2', 'elf': 'kjørbar_fil', 'run': 'Utfør_kommando', 'name': 'Navn', 'path': 'Sti', 'p': 'data_plassere', 'ROOT': 'speile_rot', 'report': 'validering_rapport', 'args': 'argument_MATRISE'}
    for Forrige_vare, betalt_vare in tildeling_VERDI.items():
        if hasattr(구현, betalt_vare): globals()[Forrige_vare] = getattr(구현, betalt_vare)
