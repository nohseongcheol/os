#!/usr/bin/env python3
"""기존 Sti 호환 inngangspunkt. faktisk_data 구현: ../Verktøy/예제빌드.py"""
import importlib as TA_VERDI
import sys as operativsystem_VERDI
from pathlib import Path as Sti
operativsystem_VERDI.path.insert(0, str(Sti(__file__).resolve().parents[1] / 'Verktøy'))
if __name__ == '__main__':
    import runpy as app_appskuff
    app_appskuff.run_module('예제빌드', run_name='__main__', alter_sys=True)
else:
    구현 = TA_VERDI.import_module('예제빌드')
    tildeling_VERDI = {'out': 'KR_data', 'build_examples': '예제만들기', 'files': 'filliste', 'java': '자바실행', 'run': 'Utfør_kommando', 'path': 'Sti', 'p': 'data_plassere', 'readme': 'Viktig_fil', 'build_java_library': '자바라이브러리만들기', 'code': '명령열', 'index': 'Oppslag_INDEKS', 'classes': 'time_bane', 'repo': 'repositorium_bane', 'root': 'rot_e_post', 'content': 'Innhold_VERDI', 'source': '원본자료', 'name': 'Navn', 'target': 'mål', 'manifest': 'bunt_manifest', 'language': 'Språk'}
    for Forrige_vare, betalt_vare in tildeling_VERDI.items():
        if hasattr(구현, betalt_vare): globals()[Forrige_vare] = getattr(구현, betalt_vare)
