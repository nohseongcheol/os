#!/usr/bin/env python3
"""기존 KELIAS 호환 įrašas_p. faktinis_duomenys 구현: ../Įrankiai/코딩시험.py"""
import importlib as TAKE_VALUE
import sys as operacinė_sistema_VALUE
from pathlib import Path as KELIAS
operacinė_sistema_VALUE.path.insert(0, str(KELIAS(__file__).resolve().parents[1] / 'Įrankiai'))
if __name__ == '__main__':
    import runpy as programa_programų_skydelis
    programa_programų_skydelis.run_module('코딩시험', run_name='__main__', alter_sys=True)
else:
    구현 = TAKE_VALUE.import_module('코딩시험')
    susiejimas_VALUE = {'out': 'KR_duomenys', 'expected': '예상결과', 'sdk': 'programuotojo_rinkinys', 'suffix': '뒷부분', 'arc': '압축묶음', 'main': 'Paleisti', 'elf': '실행파일', 'run': 'Vykdyti_komanda', 'name': 'Pavadinimas_2', 'path': 'KELIAS', 'p': 'duomenys_padėtis', 'ROOT': 'Project_šaknis', 'report': 'tikrinimas_pranešti', 'args': 'argumentas_ARRAY'}
    for 이전, dabartinis_prekė in susiejimas_VALUE.items():
        if hasattr(구현, dabartinis_prekė): globals()[이전] = getattr(구현, dabartinis_prekė)
