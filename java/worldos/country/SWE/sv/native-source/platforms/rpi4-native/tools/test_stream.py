#!/usr/bin/env python3
"""기존 sökväg_2 호환 startpunkt. verklig_data implementation: ../verktyg/test_flöde.py"""
import importlib as TA_värde
import sys as operativsystem_värde
from pathlib import Path as sökväg_2
operativsystem_värde.path.insert(0, str(sökväg_2(__file__).resolve().parents[1] / 'verktyg'))
if __name__ == '__main__':
    import runpy as app_Startbild
    app_Startbild.run_module('test_flöde', run_name='__main__', alter_sys=True)
else:
    implementation = TA_värde.import_module('test_flöde')
    mappning_värde = {'out': 'KR_data', 'main': 'Kör', 'ROOT': 'åtgärd_rot', 'p': 'data_placera', 'text': 'text', 'report': 'validering_Rapport'}
    for Föregående_objekt, aktuellt_objekt in mappning_värde.items():
        if hasattr(implementation, aktuellt_objekt): globals()[Föregående_objekt] = getattr(implementation, aktuellt_objekt)
