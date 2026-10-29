#!/usr/bin/env python3
"""기존 PUTANJA 호환 unos_p. stvaran_podaci 구현: ../Alati/SDK_programski_prevesti.py"""
import importlib as TAKE_VALUE
import sys as operacijski_sustav_VALUE
from pathlib import Path as PUTANJA
operacijski_sustav_VALUE.path.insert(0, str(PUTANJA(__file__).resolve().parents[1] / 'Alati'))
if __name__ == '__main__':
    import runpy as program_pokretač
    program_pokretač.run_module('SDK_programski_prevesti', run_name='__main__', alter_sys=True)
else:
    구현 = TAKE_VALUE.import_module('SDK_programski_prevesti')
    mapiranje_VALUE = {'compiler': 'kompilator_alat', 'obj': 'odredišna_datoteka', 'sdk': 'set_razvojnih_alata', 'output': '출력결과', 'main': 'Pokreni', 'elf': '실행파일', 'is_c': 'odjel_informacijske_tehnologije_C_Jezik', 'parser': 'analizator', 'language': 'Jezik', 'work': '작업경로', 'args': 'argument_ARRAY'}
    for 이전, redovno_artikl in mapiranje_VALUE.items():
        if hasattr(구현, redovno_artikl): globals()[이전] = getattr(구현, redovno_artikl)
