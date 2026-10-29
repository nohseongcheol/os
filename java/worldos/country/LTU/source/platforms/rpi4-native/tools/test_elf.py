#!/usr/bin/env python3
"""기존 KELIAS 호환 įrašas_p. faktinis_duomenys 구현: ../Įrankiai/실행파일시험.py"""
import importlib as TAKE_VALUE
import sys as operacinė_sistema_VALUE
from pathlib import Path as KELIAS
operacinė_sistema_VALUE.path.insert(0, str(KELIAS(__file__).resolve().parents[1] / 'Įrankiai'))
if __name__ == '__main__':
    import runpy as programa_programų_skydelis
    programa_programų_skydelis.run_module('실행파일시험', run_name='__main__', alter_sys=True)
else:
    구현 = TAKE_VALUE.import_module('실행파일시험')
    susiejimas_VALUE = {'out': 'KR_duomenys', 'expected': '예상결과', 'phoff': 'programa_Antraštė_OFFSET', 'offset': 'OFFSET_VALUE', 'invalid': 'neleistinas_duomenys', 'path': 'KELIAS', 'executable': '실행가능파일', 'rejected': '거부결과', 'linux_example': '리눅스예제', 'original': '원본', 'result': 'REZULTATAS', 'format_': 'formatas_b87fd068', 'main': 'Paleisti', 'content': 'Turinys_VALUE', 'source': '원본자료', 'name': 'Pavadinimas_2', 'reference': 'Palyginimas_bazinė_linija', 'ROOT': 'Project_šaknis', 'value': 'VALUE', 'report': 'tikrinimas_pranešti'}
    for 이전, dabartinis_prekė in susiejimas_VALUE.items():
        if hasattr(구현, dabartinis_prekė): globals()[이전] = getattr(구현, dabartinis_prekė)
