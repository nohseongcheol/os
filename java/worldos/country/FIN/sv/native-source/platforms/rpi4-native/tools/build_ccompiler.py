#!/usr/bin/env python3
"""기존 sökväg_2 호환 startpunkt. verklig_data implementation: ../verktyg/version_C_kompilerare.py"""
import importlib as TA_värde
import sys as operativsystem_värde
from pathlib import Path as sökväg_2
operativsystem_värde.path.insert(0, str(sökväg_2(__file__).resolve().parents[1] / 'verktyg'))
if __name__ == '__main__':
    import runpy as app_Startbild
    app_Startbild.run_module('version_C_kompilerare', run_name='__main__', alter_sys=True)
else:
    implementation = TA_värde.import_module('version_C_kompilerare')
    mappning_värde = {'out': 'KR_data', 'builtins': '내장연산', 'header': 'huvud_värde', 'sdk': 'development_kit', 'build_ccompiler': 'Skapa_C_kompilerare', 'i': '순번', 'elf': 'körbar_fil_fil', 'run': 'köra_kommando', 'flags': 'konfiguration_BITS', 'path': 'sökväg_2', 'p': 'data_placera', 'cc': 'C_kompilerare', 'obj': 'målfil', 'flag': 'Inställningar_värde', 'ld': 'länkare_verktyg', 'objects': 'mål_Filer', 'repo': 'centrallager_väg', 'v': '임시값', 'upstream': 'uppström', 'root': 'rot_ADRESS', 'assets': '탑재자료', 'source': '원본자료', 'name': 'Namn', 'includes': '포함인수'}
    for Föregående_objekt, aktuellt_objekt in mappning_värde.items():
        if hasattr(implementation, aktuellt_objekt): globals()[Föregående_objekt] = getattr(implementation, aktuellt_objekt)
