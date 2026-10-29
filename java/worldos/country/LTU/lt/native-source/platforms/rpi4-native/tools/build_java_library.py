#!/usr/bin/env python3
"""기존 KELIAS 호환 įrašas_p. faktinis_duomenys 구현: ../Įrankiai/자바라이브러리빌드.py"""
import importlib as TAKE_VALUE
import sys as operacinė_sistema_VALUE
from pathlib import Path as KELIAS
operacinė_sistema_VALUE.path.insert(0, str(KELIAS(__file__).resolve().parents[1] / 'Įrankiai'))
if __name__ == '__main__':
    import runpy as programa_programų_skydelis
    programa_programų_skydelis.run_module('자바라이브러리빌드', run_name='__main__', alter_sys=True)
else:
    구현 = TAKE_VALUE.import_module('자바라이브러리빌드')
    susiejimas_VALUE = {'header': 'Antraštė_VALUE', 'sources': '원문목록', 'i': '순번', 'info': 'msinfo32_exe', 'payload': 'mokamoji_krova_duomenys', 'src': '원본주소', 'run': 'Vykdyti_komanda', 'build_java_library': '자바라이브러리만들기', 'relative': 'santykinis_kelias', 'classes': 'klasė_kelias', 'dist': 'paskirstymas_kelias', 'archive': 'Archyvas', 'output': 'išeiga', 'root': 'šaknis_ADDRESS', 'name': 'Pavadinimas_2', 'jar': '자바꾸러미', 'b': 'SECOND_VALUE', 'entries': '항목들'}
    for 이전, dabartinis_prekė in susiejimas_VALUE.items():
        if hasattr(구현, dabartinis_prekė): globals()[이전] = getattr(구현, dabartinis_prekė)
