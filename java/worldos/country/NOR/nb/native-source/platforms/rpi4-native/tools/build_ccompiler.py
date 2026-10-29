#!/usr/bin/env python3
"""기존 Sti 호환 inngangspunkt. faktisk_data 구현: ../Verktøy/bygg_C_kompilator.py"""
import importlib as TA_VERDI
import sys as operativsystem_VERDI
from pathlib import Path as Sti
operativsystem_VERDI.path.insert(0, str(Sti(__file__).resolve().parents[1] / 'Verktøy'))
if __name__ == '__main__':
    import runpy as app_appskuff
    app_appskuff.run_module('bygg_C_kompilator', run_name='__main__', alter_sys=True)
else:
    구현 = TA_VERDI.import_module('bygg_C_kompilator')
    tildeling_VERDI = {'out': 'KR_data', 'builtins': '내장연산', 'header': 'Topptekst_VERDI', 'sdk': 'utviklingspakke', 'build_ccompiler': 'åpne_C_kompilator', 'i': '순번', 'elf': 'kjørbar_fil', 'run': 'Utfør_kommando', 'flags': 'konfigurasjon_BITS', 'path': 'Sti', 'p': 'data_plassere', 'cc': 'C_kompilator', 'obj': 'målfil', 'flag': 'Innstillinger_VERDI', 'ld': 'koblingsprogram_verktøy', 'objects': 'mål_Filer', 'repo': 'repositorium_bane', 'v': '임시값', 'upstream': 'oppstrøms', 'root': 'rot_e_post', 'assets': '탑재자료', 'source': '원본자료', 'name': 'Navn', 'includes': '포함인수'}
    for Forrige_vare, betalt_vare in tildeling_VERDI.items():
        if hasattr(구현, betalt_vare): globals()[Forrige_vare] = getattr(구현, betalt_vare)
