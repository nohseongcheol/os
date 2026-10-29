#!/usr/bin/env python3
"""기존 KELIAS 호환 įrašas_p. faktinis_duomenys 구현: ../Įrankiai/Vykdyti_komanda.py"""
import importlib as TAKE_VALUE
import sys as operacinė_sistema_VALUE
from pathlib import Path as KELIAS
operacinė_sistema_VALUE.path.insert(0, str(KELIAS(__file__).resolve().parents[1] / 'Įrankiai'))
if __name__ == '__main__':
    import runpy as programa_programų_skydelis
    programa_programų_skydelis.run_module('Vykdyti_komanda', run_name='__main__', alter_sys=True)
else:
    구현 = TAKE_VALUE.import_module('Vykdyti_komanda')
    susiejimas_VALUE = {'supported': '지원목록', 'parser': 'analizatorius', 'qemu': '모의기계', 'run_desktop': 'vykdyti_darbalaukis', 'main': 'Paleisti', 'host': 'organizuoti', 'status': 'Būsena_VALUE', 'NetworkBridge': 'tiltas_3de4fe3a', 'ROOT': 'Project_šaknis', 'bridge': 'tiltas', 'loader': 'įkelties_programa', 'base': 'Fonas_VALUE', 'options': 'Parinktys', 'binary': 'dvejetainis', 'args': 'argumentas_ARRAY', 'command': 'Komanda'}
    for 이전, dabartinis_prekė in susiejimas_VALUE.items():
        if hasattr(구현, dabartinis_prekė): globals()[이전] = getattr(구현, dabartinis_prekė)
