#!/usr/bin/env python3
"""기존 sökväg_2 호환 startpunkt. verklig_data implementation: ../verktyg/코딩시험.py"""
import importlib as TA_värde
import sys as operativsystem_värde
from pathlib import Path as sökväg_2
operativsystem_värde.path.insert(0, str(sökväg_2(__file__).resolve().parents[1] / 'verktyg'))
if __name__ == '__main__':
    import runpy as app_Startbild
    app_Startbild.run_module('코딩시험', run_name='__main__', alter_sys=True)
else:
    implementation = TA_värde.import_module('코딩시험')
    mappning_värde = {'out': 'KR_data', 'expected': '예상결과', 'sdk': 'development_kit', 'suffix': '뒷부분', 'arc': '압축묶음', 'main': 'Kör', 'elf': 'körbar_fil_fil', 'run': 'köra_kommando', 'name': 'Namn', 'path': 'sökväg_2', 'p': 'data_placera', 'ROOT': 'åtgärd_rot', 'report': 'validering_Rapport', 'args': 'argument_MATRIS'}
    for Föregående_objekt, aktuellt_objekt in mappning_värde.items():
        if hasattr(implementation, aktuellt_objekt): globals()[Föregående_objekt] = getattr(implementation, aktuellt_objekt)
