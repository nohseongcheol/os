#!/usr/bin/env python3
"""기존 PUTANJA 호환 unos_p. stvaran_podaci 구현: ../Alati/izvezi_SDK.py"""
import importlib as TAKE_VALUE
import sys as operacijski_sustav_VALUE
from pathlib import Path as PUTANJA
operacijski_sustav_VALUE.path.insert(0, str(PUTANJA(__file__).resolve().parents[1] / 'Alati'))
if __name__ == '__main__':
    import runpy as program_pokretač
    program_pokretač.run_module('izvezi_SDK', run_name='__main__', alter_sys=True)
else:
    구현 = TAKE_VALUE.import_module('izvezi_SDK')
    mapiranje_VALUE = {'out': 'KR_podaci', 'obj': 'odredišna_datoteka', 'relative': 'relativni_put', 'compiler_archive': 'kompilator_Arhiva', 'sdk': 'set_razvojnih_alata', 'dist': '배포경로', 'archive': 'Arhiva', 'main': 'Pokreni', 'posix': '포직스경로', 'files': 'Datoteka_Popis', 'source': '원본자료', 'name': 'Ime', 'target': 'cilj', 'ROOT': 'akcija_korijen', 'destination': 'odredište_podaci_adresa', 'manifest': '꾸러미명세', 'work': '작업경로'}
    for 이전, redovno_artikl in mapiranje_VALUE.items():
        if hasattr(구현, redovno_artikl): globals()[이전] = getattr(구현, redovno_artikl)
