#!/usr/bin/env python3
"""기존 Putanja 호환 unos_p. stvaran_podaci 구현: ../Alati/izvesti_SDK.py"""
import importlib as TAKE_VALUE
import sys as operativni_sistem_VALUE
from pathlib import Path as Putanja
operativni_sistem_VALUE.path.insert(0, str(Putanja(__file__).resolve().parents[1] / 'Alati'))
if __name__ == '__main__':
    import runpy as program_pokretač
    program_pokretač.run_module('izvesti_SDK', run_name='__main__', alter_sys=True)
else:
    구현 = TAKE_VALUE.import_module('izvesti_SDK')
    대응 = {'out': 'mjera_podaci', 'obj': 'odredišni_fajl', 'relative': '상대경로', 'compiler_archive': '번역기꾸러미', 'sdk': '개발꾸러미', 'dist': '배포경로', 'archive': 'Arhiva', 'main': 'Pokreni', 'posix': '포직스경로', 'files': 'fajl_spisak', 'source': '원본자료', 'name': 'Naziv', 'target': 'cilj', 'ROOT': 'projicirati_koijen', 'destination': 'odredište_podaci_adresa', 'manifest': '꾸러미명세', 'work': '작업경로'}
    for 이전, trenutno_stavka in 대응.items():
        if hasattr(구현, trenutno_stavka): globals()[이전] = getattr(구현, trenutno_stavka)
