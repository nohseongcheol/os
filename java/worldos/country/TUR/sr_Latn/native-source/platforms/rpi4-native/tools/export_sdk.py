#!/usr/bin/env python3
"""기존 putanja 호환 stavka_p. stvarni_podaci 구현: ../Alatke/izvesti_SDK.py"""
import importlib as TAKE_VALUE
import sys as operativni_sistem_VALUE
from pathlib import Path as putanja
operativni_sistem_VALUE.path.insert(0, str(putanja(__file__).resolve().parents[1] / 'Alatke'))
if __name__ == '__main__':
    import runpy as program_pokretač
    program_pokretač.run_module('izvesti_SDK', run_name='__main__', alter_sys=True)
else:
    구현 = TAKE_VALUE.import_module('izvesti_SDK')
    mapiranje_VALUE = {'out': 'KR_podaci', 'obj': 'odredišna_datoteka', 'relative': 'relativna_putanja', 'compiler_archive': 'kompajler_Arhiva', 'sdk': 'komplet_za_razvoj_programa', 'dist': '배포경로', 'archive': 'Arhiva', 'main': 'koristiti', 'posix': '포직스경로', 'files': 'Datoteka_Lista', 'source': '원본자료', 'name': 'ime', 'target': 'cilj', 'ROOT': 'radnja_koren', 'destination': 'odredište_podaci_adresa', 'manifest': '꾸러미명세', 'work': '작업경로'}
    for 이전, aktuelno_stavka in mapiranje_VALUE.items():
        if hasattr(구현, aktuelno_stavka): globals()[이전] = getattr(구현, aktuelno_stavka)
