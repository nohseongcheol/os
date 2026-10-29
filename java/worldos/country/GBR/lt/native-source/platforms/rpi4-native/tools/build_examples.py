#!/usr/bin/env python3
"""기존 KELIAS 호환 įrašas_p. faktinis_duomenys 구현: ../Įrankiai/예제빌드.py"""
import importlib as TAKE_VALUE
import sys as operacinė_sistema_VALUE
from pathlib import Path as KELIAS
operacinė_sistema_VALUE.path.insert(0, str(KELIAS(__file__).resolve().parents[1] / 'Įrankiai'))
if __name__ == '__main__':
    import runpy as programa_programų_skydelis
    programa_programų_skydelis.run_module('예제빌드', run_name='__main__', alter_sys=True)
else:
    구현 = TAKE_VALUE.import_module('예제빌드')
    susiejimas_VALUE = {'out': 'KR_duomenys', 'build_examples': '예제만들기', 'files': 'Failas_Sąrašas', 'java': '자바실행', 'run': 'Vykdyti_komanda', 'path': 'KELIAS', 'p': 'duomenys_padėtis', 'readme': '안내자료', 'build_java_library': '자바라이브러리만들기', 'code': '명령열', 'index': 'LOOKUP_INDEX', 'classes': 'klasė_kelias', 'repo': 'saugykla_kelias', 'root': 'šaknis_ADDRESS', 'content': 'Turinys_VALUE', 'source': '원본자료', 'name': 'Pavadinimas_2', 'target': 'tikslas', 'manifest': '꾸러미명세', 'language': 'Kalba'}
    for 이전, dabartinis_prekė in susiejimas_VALUE.items():
        if hasattr(구현, dabartinis_prekė): globals()[이전] = getattr(구현, dabartinis_prekė)
