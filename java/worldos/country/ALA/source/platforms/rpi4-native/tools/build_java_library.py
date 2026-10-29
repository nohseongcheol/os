#!/usr/bin/env python3
"""기존 sökväg_2 호환 startpunkt. verklig_data implementation: ../verktyg/자바라이브러리빌드.py"""
import importlib as TA_värde
import sys as operativsystem_värde
from pathlib import Path as sökväg_2
operativsystem_värde.path.insert(0, str(sökväg_2(__file__).resolve().parents[1] / 'verktyg'))
if __name__ == '__main__':
    import runpy as app_Startbild
    app_Startbild.run_module('자바라이브러리빌드', run_name='__main__', alter_sys=True)
else:
    implementation = TA_värde.import_module('자바라이브러리빌드')
    mappning_värde = {'header': 'huvud_värde', 'sources': '원문목록', 'i': '순번', 'info': 'msinfo32_exe', 'payload': 'nyttolast_data', 'src': '원본주소', 'run': 'köra_kommando', 'build_java_library': '자바라이브러리만들기', 'relative': 'relativ_sökväg', 'classes': 'Kurs_väg', 'dist': 'fördelning_väg', 'archive': 'Arkiv', 'output': 'utleverans', 'root': 'rot_ADRESS', 'name': 'Namn', 'jar': '자바꾸러미', 'b': 'SEKUND_värde', 'entries': '항목들'}
    for Föregående_objekt, aktuellt_objekt in mappning_värde.items():
        if hasattr(implementation, aktuellt_objekt): globals()[Föregående_objekt] = getattr(implementation, aktuellt_objekt)
