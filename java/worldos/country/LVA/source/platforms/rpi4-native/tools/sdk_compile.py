#!/usr/bin/env python3
"""기존 CEĻŠ 호환 ieejas_punkts. faktisks_dati 구현: ../Rīki/SDK_kompilēt.py"""
import importlib as TAKE_VALUE
import sys as operētājsistēma_VALUE
from pathlib import Path as CEĻŠ
operētājsistēma_VALUE.path.insert(0, str(CEĻŠ(__file__).resolve().parents[1] / 'Rīki'))
if __name__ == '__main__':
    import runpy as programma_palaidējs
    programma_palaidējs.run_module('SDK_kompilēt', run_name='__main__', alter_sys=True)
else:
    구현 = TAKE_VALUE.import_module('SDK_kompilēt')
    kartēšana_VALUE = {'compiler': 'kompilators_rīks', 'obj': 'mērķa_fails', 'sdk': 'programmizstrādes_komplekts', 'output': 'ražojums', 'main': 'Palaist', 'elf': 'izpildāms_fails', 'is_c': 'informācijas_tehnoloģija_C_Valodas', 'parser': 'parsētājs', 'language': 'Valodas', 'work': '작업경로', 'args': 'arg_ARRAY'}
    for 이전, pašreizējais_krājums in kartēšana_VALUE.items():
        if hasattr(구현, pašreizējais_krājums): globals()[이전] = getattr(구현, pašreizējais_krājums)
