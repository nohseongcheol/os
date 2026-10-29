#!/usr/bin/env python3
"""기존 sökväg_2 호환 startpunkt. verklig_data implementation: ../verktyg/version_nätverk.py"""
import importlib as TA_värde
import sys as operativsystem_värde
from pathlib import Path as sökväg_2
operativsystem_värde.path.insert(0, str(sökväg_2(__file__).resolve().parents[1] / 'verktyg'))
if __name__ == '__main__':
    import runpy as app_Startbild
    app_Startbild.run_module('version_nätverk', run_name='__main__', alter_sys=True)
else:
    implementation = TA_värde.import_module('version_nätverk')
    mappning_värde = {'obj': 'målfil', 'objects': 'mål_Filer', 'library': 'bibliotek', 'output': 'utleverans', 'port': 'portnummer', 'root': 'rot_ADRESS', 'files': 'fillista', 'source': '원본자료', 'run': 'köra_kommando', 'flags': 'konfiguration_BITS', 'path': 'sökväg_2', 'build_network': 'Skapa_nätverk', 'cc': 'C_kompilerare', 'ar': 'Arkiv_verktyg'}
    for Föregående_objekt, aktuellt_objekt in mappning_värde.items():
        if hasattr(implementation, aktuellt_objekt): globals()[Föregående_objekt] = getattr(implementation, aktuellt_objekt)
