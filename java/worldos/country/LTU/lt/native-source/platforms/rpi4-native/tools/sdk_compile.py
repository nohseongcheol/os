#!/usr/bin/env python3
"""기존 KELIAS 호환 įrašas_p. faktinis_duomenys 구현: ../Įrankiai/SDK_kompiliuoti.py"""
import importlib as TAKE_VALUE
import sys as operacinė_sistema_VALUE
from pathlib import Path as KELIAS
operacinė_sistema_VALUE.path.insert(0, str(KELIAS(__file__).resolve().parents[1] / 'Įrankiai'))
if __name__ == '__main__':
    import runpy as programa_programų_skydelis
    programa_programų_skydelis.run_module('SDK_kompiliuoti', run_name='__main__', alter_sys=True)
else:
    구현 = TAKE_VALUE.import_module('SDK_kompiliuoti')
    susiejimas_VALUE = {'compiler': 'kompiliatorius_įrankis', 'obj': 'paskirties_failas', 'sdk': 'programuotojo_rinkinys', 'output': 'išeiga', 'main': 'Paleisti', 'elf': '실행파일', 'is_c': 'informacinės_technologijos_C_Kalba', 'parser': 'analizatorius', 'language': 'Kalba', 'work': '작업경로', 'args': 'argumentas_ARRAY'}
    for 이전, dabartinis_prekė in susiejimas_VALUE.items():
        if hasattr(구현, dabartinis_prekė): globals()[이전] = getattr(구현, dabartinis_prekė)
