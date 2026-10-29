#!/usr/bin/env python3
"""기존 Sti 호환 indgangspunkt. faktisk_data 구현: ../Værktøjer/eksportere_SDK.py"""
import importlib as TAG_VÆRDI
import sys as operativsystem_VÆRDI
from pathlib import Path as Sti
operativsystem_VÆRDI.path.insert(0, str(Sti(__file__).resolve().parents[1] / 'Værktøjer'))
if __name__ == '__main__':
    import runpy as app_Kvikstart
    app_Kvikstart.run_module('eksportere_SDK', run_name='__main__', alter_sys=True)
else:
    구현 = TAG_VÆRDI.import_module('eksportere_SDK')
    tilknytning_VÆRDI = {'out': 'KR_data', 'obj': 'destinationsfil', 'relative': 'relativ_sti', 'compiler_archive': 'compiler_Arkiv', 'sdk': 'Development_Kit', 'dist': 'distribution_sti', 'archive': 'Arkiv', 'main': 'Kør_2', 'posix': '포직스경로', 'files': 'filliste', 'source': '원본자료', 'name': 'Navn', 'target': 'mål', 'ROOT': 'To_do_rod', 'destination': 'destination_data_mail', 'manifest': 'bundt_manifest', 'work': '작업경로'}
    for Forrige_vare, aktuel_vare in tilknytning_VÆRDI.items():
        if hasattr(구현, aktuel_vare): globals()[Forrige_vare] = getattr(구현, aktuel_vare)
