#!/usr/bin/env python3
"""기존 CEĻŠ 호환 ieejas_punkts. faktisks_dati 구현: ../Rīki/Izpildīt_komanda.py"""
import importlib as TAKE_VALUE
import sys as operētājsistēma_VALUE
from pathlib import Path as CEĻŠ
operētājsistēma_VALUE.path.insert(0, str(CEĻŠ(__file__).resolve().parents[1] / 'Rīki'))
if __name__ == '__main__':
    import runpy as programma_palaidējs
    programma_palaidējs.run_module('Izpildīt_komanda', run_name='__main__', alter_sys=True)
else:
    구현 = TAKE_VALUE.import_module('Izpildīt_komanda')
    kartēšana_VALUE = {'supported': '지원목록', 'parser': 'parsētājs', 'qemu': '모의기계', 'run_desktop': 'virkne_dators', 'main': 'Palaist', 'host': 'viesot', 'status': 'Statuss_VALUE', 'NetworkBridge': 'tilts_3de4fe3a', 'ROOT': 'Project_sakne', 'bridge': 'tilts', 'loader': 'ielādētājs', 'base': 'Fons_VALUE', 'options': 'Opcijas', 'binary': 'binary', 'args': 'arg_ARRAY', 'command': 'Komanda'}
    for 이전, pašreizējais_krājums in kartēšana_VALUE.items():
        if hasattr(구현, pašreizējais_krājums): globals()[이전] = getattr(구현, pašreizējais_krājums)
