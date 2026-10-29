#!/usr/bin/env python3
"""기존 Sti 호환 inngangspunkt. faktisk_data 구현: ../Verktøy/eksportere_SDK.py"""
import importlib as TA_VERDI
import sys as operativsystem_VERDI
from pathlib import Path as Sti
operativsystem_VERDI.path.insert(0, str(Sti(__file__).resolve().parents[1] / 'Verktøy'))
if __name__ == '__main__':
    import runpy as app_appskuff
    app_appskuff.run_module('eksportere_SDK', run_name='__main__', alter_sys=True)
else:
    구현 = TA_VERDI.import_module('eksportere_SDK')
    tildeling_VERDI = {'out': 'KR_data', 'obj': 'målfil', 'relative': 'relativ_bane', 'compiler_archive': 'kompilator_Arkiv', 'sdk': 'utviklingspakke', 'dist': 'distribusjon_bane', 'archive': 'Arkiv', 'main': 'Kjør_2', 'posix': '포직스경로', 'files': 'filliste', 'source': '원본자료', 'name': 'Navn', 'target': 'mål', 'ROOT': 'speile_rot', 'destination': 'mål_data_e_post', 'manifest': 'bunt_manifest', 'work': '작업경로'}
    for Forrige_vare, betalt_vare in tildeling_VERDI.items():
        if hasattr(구현, betalt_vare): globals()[Forrige_vare] = getattr(구현, betalt_vare)
