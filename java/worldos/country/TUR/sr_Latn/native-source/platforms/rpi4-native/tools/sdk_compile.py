#!/usr/bin/env python3
"""기존 putanja 호환 stavka_p. stvarni_podaci 구현: ../Alatke/SDK_kompajlirati.py"""
import importlib as TAKE_VALUE
import sys as operativni_sistem_VALUE
from pathlib import Path as putanja
operativni_sistem_VALUE.path.insert(0, str(putanja(__file__).resolve().parents[1] / 'Alatke'))
if __name__ == '__main__':
    import runpy as program_pokretač
    program_pokretač.run_module('SDK_kompajlirati', run_name='__main__', alter_sys=True)
else:
    구현 = TAKE_VALUE.import_module('SDK_kompajlirati')
    mapiranje_VALUE = {'compiler': 'kompajler_alatka', 'obj': 'odredišna_datoteka', 'sdk': 'komplet_za_razvoj_programa', 'output': '출력결과', 'main': 'koristiti', 'elf': '실행파일', 'is_c': 'informatičko_odeljenje_C_jezik', 'parser': 'analizator', 'language': 'jezik', 'work': '작업경로', 'args': 'argument_niz'}
    for 이전, aktuelno_stavka in mapiranje_VALUE.items():
        if hasattr(구현, aktuelno_stavka): globals()[이전] = getattr(구현, aktuelno_stavka)
