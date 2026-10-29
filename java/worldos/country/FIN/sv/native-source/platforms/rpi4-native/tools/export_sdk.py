#!/usr/bin/env python3
"""기존 sökväg_2 호환 startpunkt. verklig_data implementation: ../verktyg/exportera_SDK.py"""
import importlib as TA_värde
import sys as operativsystem_värde
from pathlib import Path as sökväg_2
operativsystem_värde.path.insert(0, str(sökväg_2(__file__).resolve().parents[1] / 'verktyg'))
if __name__ == '__main__':
    import runpy as app_Startbild
    app_Startbild.run_module('exportera_SDK', run_name='__main__', alter_sys=True)
else:
    implementation = TA_värde.import_module('exportera_SDK')
    mappning_värde = {'out': 'KR_data', 'obj': 'målfil', 'relative': 'relativ_sökväg', 'compiler_archive': 'kompilerare_Arkiv', 'sdk': 'development_kit', 'dist': 'fördelning_väg', 'archive': 'Arkiv', 'main': 'Kör', 'posix': '포직스경로', 'files': 'fillista', 'source': '원본자료', 'name': 'Namn', 'target': 'mål', 'ROOT': 'åtgärd_rot', 'destination': 'mål_data_ADRESS', 'manifest': 'bunt_manifest', 'work': '작업경로'}
    for Föregående_objekt, aktuellt_objekt in mappning_värde.items():
        if hasattr(implementation, aktuellt_objekt): globals()[Föregående_objekt] = getattr(implementation, aktuellt_objekt)
