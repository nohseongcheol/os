#!/usr/bin/env python3
"""기존 CEĻŠ 호환 ieejas_punkts. faktisks_dati 구현: ../Rīki/Upload_Faili.py"""
import importlib as TAKE_VALUE
import sys as operētājsistēma_VALUE
from pathlib import Path as CEĻŠ
operētājsistēma_VALUE.path.insert(0, str(CEĻŠ(__file__).resolve().parents[1] / 'Rīki'))
if __name__ == '__main__':
    import runpy as programma_palaidējs
    programma_palaidējs.run_module('Upload_Faili', run_name='__main__', alter_sys=True)
else:
    구현 = TAKE_VALUE.import_module('Upload_Faili')
    kartēšana_VALUE = {'data': 'dati', 'i': '순번', 'name': 'Nosaukums', 'c': 'koda_punkts', 'p': 'dati_amats', 'args': 'arg_ARRAY'}
    for 이전, pašreizējais_krājums in kartēšana_VALUE.items():
        if hasattr(구현, pašreizējais_krājums): globals()[이전] = getattr(구현, pašreizējais_krājums)
