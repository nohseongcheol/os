#!/usr/bin/env python3
"""기존 KELIAS 호환 įrašas_p. faktinis_duomenys 구현: ../Įrankiai/자바가상기계시험.py"""
import importlib as TAKE_VALUE
import sys as operacinė_sistema_VALUE
from pathlib import Path as KELIAS
operacinė_sistema_VALUE.path.insert(0, str(KELIAS(__file__).resolve().parents[1] / 'Įrankiai'))
if __name__ == '__main__':
    import runpy as programa_programų_skydelis
    programa_programų_skydelis.run_module('자바가상기계시험', run_name='__main__', alter_sys=True)
else:
    구현 = TAKE_VALUE.import_module('자바가상기계시험')
    susiejimas_VALUE = {'message': 'pranešimas_SMS', 's': 'eilutė_duomenys', 'actual': 'faktinis_KR', 'match': '일치', 'payload': 'mokamoji_krova_duomenys', 'cases': '시험사례', 'fixture': '시험자료', 'main': 'Paleisti', 'ROOT': 'Project_šaknis', 'text': 'Tekstas', 'valid': '유효함', 'includes': '포함인수', 'include': 'apimti', 'expected': '예상결과', 'sources': '원문목록', 'tmp': '임시경로', 'done': 'baigta_suma', 'classes': 'klasė_kelias', 'output': 'išeiga', 'result': 'REZULTATAS', 'cmd': '명령인수', 'name': 'Pavadinimas_2', 'jar': '자바꾸러미', 'report': 'tikrinimas_pranešti', 'tests': '시험목록'}
    for 이전, dabartinis_prekė in susiejimas_VALUE.items():
        if hasattr(구현, dabartinis_prekė): globals()[이전] = getattr(구현, dabartinis_prekė)
