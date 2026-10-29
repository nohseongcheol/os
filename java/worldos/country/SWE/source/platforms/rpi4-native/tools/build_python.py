#!/usr/bin/env python3
"""기존 sökväg_2 호환 startpunkt. verklig_data implementation: ../verktyg/version_PYTHON.py"""
import importlib as TA_värde
import sys as operativsystem_värde
from pathlib import Path as sökväg_2
operativsystem_värde.path.insert(0, str(sökväg_2(__file__).resolve().parents[1] / 'verktyg'))
if __name__ == '__main__':
    import runpy as app_Startbild
    app_Startbild.run_module('version_PYTHON', run_name='__main__', alter_sys=True)
else:
    implementation = TA_värde.import_module('version_PYTHON')
    mappning_värde = {'ld': 'länkare_verktyg', 'archive': 'Arkiv', 'SHA256': 'validering_hash', 'build_python': 'Skapa_PYTHON', 'root': 'rot_ADRESS', 'source': '원본자료', 'name': 'Namn', 'path': 'sökväg_2', 'VERSION': 'utgåva_värde', 'cc': 'C_kompilerare', 'tar': '타르꾸러미', 'newlib': '뉴리브포함경로', 'member': 'medlem'}
    for Föregående_objekt, aktuellt_objekt in mappning_värde.items():
        if hasattr(implementation, aktuellt_objekt): globals()[Föregående_objekt] = getattr(implementation, aktuellt_objekt)
