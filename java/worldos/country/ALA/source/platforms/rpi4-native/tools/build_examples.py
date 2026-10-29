#!/usr/bin/env python3
"""기존 sökväg_2 호환 startpunkt. verklig_data implementation: ../verktyg/예제빌드.py"""
import importlib as TA_värde
import sys as operativsystem_värde
from pathlib import Path as sökväg_2
operativsystem_värde.path.insert(0, str(sökväg_2(__file__).resolve().parents[1] / 'verktyg'))
if __name__ == '__main__':
    import runpy as app_Startbild
    app_Startbild.run_module('예제빌드', run_name='__main__', alter_sys=True)
else:
    implementation = TA_värde.import_module('예제빌드')
    mappning_värde = {'out': 'KR_data', 'build_examples': '예제만들기', 'files': 'fillista', 'java': '자바실행', 'run': 'köra_kommando', 'path': 'sökväg_2', 'p': 'data_placera', 'readme': 'VIKTIGT', 'build_java_library': '자바라이브러리만들기', 'code': 'instruktion_SEKVENS', 'index': 'LETAUPP_INDEX', 'classes': 'Kurs_väg', 'repo': 'centrallager_väg', 'root': 'rot_ADRESS', 'content': 'Innehåll_värde', 'source': '원본자료', 'name': 'Namn', 'target': 'mål', 'manifest': 'bunt_manifest', 'language': 'Språk'}
    for Föregående_objekt, aktuellt_objekt in mappning_värde.items():
        if hasattr(implementation, aktuellt_objekt): globals()[Föregående_objekt] = getattr(implementation, aktuellt_objekt)
