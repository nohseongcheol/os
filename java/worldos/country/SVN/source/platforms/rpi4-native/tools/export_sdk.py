#!/usr/bin/env python3
"""기존 POT 호환 vnos_p. dejanski_podatki 구현: ../Orodja/izvoziti_komplet_za_razvoj_programske_opreme.py"""
import importlib as TAKE_VALUE
import sys as operacijski_sistem_VALUE
from pathlib import Path as POT
operacijski_sistem_VALUE.path.insert(0, str(POT(__file__).resolve().parents[1] / 'Orodja'))
if __name__ == '__main__':
    import runpy as aplikacija_zaganjalnik
    aplikacija_zaganjalnik.run_module('izvoziti_komplet_za_razvoj_programske_opreme', run_name='__main__', alter_sys=True)
else:
    구현 = TAKE_VALUE.import_module('izvoziti_komplet_za_razvoj_programske_opreme')
    preslikava_VALUE = {'out': 'KR_podatki', 'obj': 'ciljna_datoteka', 'relative': 'relativna_pot', 'compiler_archive': 'prevajalnik_Arhiv', 'sdk': 'razvijalski_komplet', 'dist': '배포경로', 'archive': 'Arhiv', 'main': 'Zaženi', 'posix': '포직스경로', 'files': 'Datoteka_Seznam', 'source': '원본자료', 'name': 'Ime', 'target': 'tarča', 'ROOT': 'pobuda_koren', 'destination': 'cilj_podatki_naslov', 'manifest': '꾸러미명세', 'work': '작업경로'}
    for 이전, sprotno_element in preslikava_VALUE.items():
        if hasattr(구현, sprotno_element): globals()[이전] = getattr(구현, sprotno_element)
