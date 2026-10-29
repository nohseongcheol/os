#!/usr/bin/env python3
"""기존 KELIAS 호환 įrašas_p. faktinis_duomenys 구현: ../Įrankiai/되돌림시험서버.py"""
import importlib as TAKE_VALUE
import sys as operacinė_sistema_VALUE
from pathlib import Path as KELIAS
operacinė_sistema_VALUE.path.insert(0, str(KELIAS(__file__).resolve().parents[1] / 'Įrankiai'))
if __name__ == '__main__':
    import runpy as programa_programų_skydelis
    programa_programų_skydelis.run_module('되돌림시험서버', run_name='__main__', alter_sys=True)
else:
    구현 = TAKE_VALUE.import_module('되돌림시험서버')
    susiejimas_VALUE = {'data': 'duomenys', 'e': '보조항목', 'connection': 'ryšys_e05f319b', 'f': 'Failas_įrašas', 'peer': 'lygiavertis_mazgas_VALUE', 'self': '자신', 'udp': 'paketų_kelio_schema_valdymas', 't': 'Terminalas_įrašas', 'tcp': 'ryšys_valdymas', 'EchoFixture': '되돌림시험서버', 'args': 'argumentas_ARRAY', 'chunk': '조각'}
    for 이전, dabartinis_prekė in susiejimas_VALUE.items():
        if hasattr(구현, dabartinis_prekė): globals()[이전] = getattr(구현, dabartinis_prekė)
