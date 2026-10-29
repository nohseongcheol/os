#!/usr/bin/env python3
"""기존 CEĻŠ 호환 ieejas_punkts. faktisks_dati 구현: ../Rīki/코딩시험.py"""
import importlib as TAKE_VALUE
import sys as operētājsistēma_VALUE
from pathlib import Path as CEĻŠ
operētājsistēma_VALUE.path.insert(0, str(CEĻŠ(__file__).resolve().parents[1] / 'Rīki'))
if __name__ == '__main__':
    import runpy as programma_palaidējs
    programma_palaidējs.run_module('코딩시험', run_name='__main__', alter_sys=True)
else:
    구현 = TAKE_VALUE.import_module('코딩시험')
    kartēšana_VALUE = {'out': 'mērs_dati', 'expected': '예상결과', 'sdk': 'programmizstrādes_komplekts', 'suffix': '뒷부분', 'arc': '압축묶음', 'main': 'Palaist', 'elf': 'izpildāms_fails', 'run': 'Izpildīt_komanda', 'name': 'Nosaukums', 'path': 'CEĻŠ', 'p': 'dati_amats', 'ROOT': 'Project_sakne', 'report': 'validācija_ziņot', 'args': 'arg_ARRAY'}
    for 이전, pašreizējais_krājums in kartēšana_VALUE.items():
        if hasattr(구현, pašreizējais_krājums): globals()[이전] = getattr(구현, pašreizējais_krājums)
