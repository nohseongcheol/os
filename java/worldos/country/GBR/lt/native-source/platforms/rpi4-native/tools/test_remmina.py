#!/usr/bin/env python3
"""기존 KELIAS 호환 įrašas_p. faktinis_duomenys 구현: ../Įrankiai/원격한글시험.py"""
import importlib as TAKE_VALUE
import sys as operacinė_sistema_VALUE
from pathlib import Path as KELIAS
operacinė_sistema_VALUE.path.insert(0, str(KELIAS(__file__).resolve().parents[1] / 'Įrankiai'))
if __name__ == '__main__':
    import runpy as programa_programų_skydelis
    programa_programų_skydelis.run_module('원격한글시험', run_name='__main__', alter_sys=True)
else:
    구현 = TAKE_VALUE.import_module('원격한글시험')
    susiejimas_VALUE = {'wait': '기다리기', 'typing': '글자입력', 'start': 'Paleisti', 'profile': 'Profilis', 'focused': 'Reikšmingiausi', 'serial': '직렬입출력', 'keys': '누름열', 'server': 'serveris_VALUE', 'log': 'LOG_RECORD', 'args': 'argumentas_ARRAY', 'deadline': 'terminas_TIME', 'data': 'duomenys', 'candidate': '후보', 'logs': '기록들', 'kw': 'įvardytasis_argumentas', 'number': '수치', 'main': 'Paleisti', 'ready': '준비완료', 'found': 'Ieška_KR', 'guest': 'svečias', 'ROOT': 'Project_šaknis', 'marker': 'žymeklis', 'text': 'Tekstas', 'out': 'KR_duomenys', 'env': '환경', 'f': 'Failas_įrašas', 'port': 'prievado_numeris', 'offset': 'OFFSET_VALUE', 'version': 'versijos_numeris', 'p': 'duomenys_padėtis', 'selector': 'išrinkiklis', 'xvfb': '가상표시장치', 'display': 'ekranas', 'n': 'prekė_COUNT', 'key': '누름값', 'processes': '실행과정들', 'rootfs': '뿌리파일계층', 'xdo': '가상입력도구', 'name': 'Pavadinimas_2', 'window': 'Langas', 'report': 'tikrinimas_pranešti', 'work': '작업경로'}
    for 이전, dabartinis_prekė in susiejimas_VALUE.items():
        if hasattr(구현, dabartinis_prekė): globals()[이전] = getattr(구현, dabartinis_prekė)
