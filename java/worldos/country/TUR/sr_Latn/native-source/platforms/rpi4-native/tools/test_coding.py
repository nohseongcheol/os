#!/usr/bin/env python3
"""기존 putanja 호환 stavka_p. stvarni_podaci 구현: ../Alatke/코딩시험.py"""
import importlib as TAKE_VALUE
import sys as operativni_sistem_VALUE
from pathlib import Path as putanja
operativni_sistem_VALUE.path.insert(0, str(putanja(__file__).resolve().parents[1] / 'Alatke'))
if __name__ == '__main__':
    import runpy as program_pokretač
    program_pokretač.run_module('코딩시험', run_name='__main__', alter_sys=True)
else:
    구현 = TAKE_VALUE.import_module('코딩시험')
    mapiranje_VALUE = {'out': 'KR_podaci', 'expected': '예상결과', 'sdk': 'komplet_za_razvoj_programa', 'suffix': '뒷부분', 'arc': '압축묶음', 'main': 'koristiti', 'elf': '실행파일', 'run': 'Izvrši_komanda', 'name': 'ime', 'path': 'putanja', 'p': 'podaci_pozicija', 'ROOT': 'radnja_koren', 'report': 'provera_valjanosti_izveštaj', 'args': 'argument_niz'}
    for 이전, aktuelno_stavka in mapiranje_VALUE.items():
        if hasattr(구현, aktuelno_stavka): globals()[이전] = getattr(구현, aktuelno_stavka)
