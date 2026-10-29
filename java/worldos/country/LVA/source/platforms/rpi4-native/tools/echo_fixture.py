#!/usr/bin/env python3
"""기존 CEĻŠ 호환 ieejas_punkts. faktisks_dati 구현: ../Rīki/되돌림시험서버.py"""
import importlib as TAKE_VALUE
import sys as operētājsistēma_VALUE
from pathlib import Path as CEĻŠ
operētājsistēma_VALUE.path.insert(0, str(CEĻŠ(__file__).resolve().parents[1] / 'Rīki'))
if __name__ == '__main__':
    import runpy as programma_palaidējs
    programma_palaidējs.run_module('되돌림시험서버', run_name='__main__', alter_sys=True)
else:
    구현 = TAKE_VALUE.import_module('되돌림시험서버')
    kartēšana_VALUE = {'data': 'dati', 'e': '보조항목', 'connection': 'paziņa_e05f319b', 'f': 'Fails_ievade', 'peer': 'vienranga_VALUE', 'self': '자신', 'udp': 'datogramma_vadība', 't': 'Terminālis_ievade', 'tcp': 'paziņa_vadība', 'EchoFixture': '되돌림시험서버', 'args': 'arg_ARRAY', 'chunk': '조각'}
    for 이전, pašreizējais_krājums in kartēšana_VALUE.items():
        if hasattr(구현, pašreizējais_krājums): globals()[이전] = getattr(구현, pašreizējais_krājums)
