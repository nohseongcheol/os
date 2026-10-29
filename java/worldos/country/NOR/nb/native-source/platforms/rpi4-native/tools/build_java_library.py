#!/usr/bin/env python3
"""기존 Sti 호환 inngangspunkt. faktisk_data 구현: ../Verktøy/자바라이브러리빌드.py"""
import importlib as TA_VERDI
import sys as operativsystem_VERDI
from pathlib import Path as Sti
operativsystem_VERDI.path.insert(0, str(Sti(__file__).resolve().parents[1] / 'Verktøy'))
if __name__ == '__main__':
    import runpy as app_appskuff
    app_appskuff.run_module('자바라이브러리빌드', run_name='__main__', alter_sys=True)
else:
    구현 = TA_VERDI.import_module('자바라이브러리빌드')
    tildeling_VERDI = {'header': 'Topptekst_VERDI', 'sources': '원문목록', 'i': '순번', 'info': 'msinfo32_exe', 'payload': 'nyttelast_data', 'src': '원본주소', 'run': 'Utfør_kommando', 'build_java_library': '자바라이브러리만들기', 'relative': 'relativ_bane', 'classes': 'time_bane', 'dist': 'distribusjon_bane', 'archive': 'Arkiv', 'output': 'produksjon', 'root': 'rot_e_post', 'name': 'Navn', 'jar': '자바꾸러미', 'b': 'SEKUND_VERDI', 'entries': '항목들'}
    for Forrige_vare, betalt_vare in tildeling_VERDI.items():
        if hasattr(구현, betalt_vare): globals()[Forrige_vare] = getattr(구현, betalt_vare)
