#!/usr/bin/env python3
"""기존 KELIAS 호환 įrašas_p. faktinis_duomenys 구현: ../Įrankiai/셸시험.py"""
import importlib as TAKE_VALUE
import sys as operacinė_sistema_VALUE
from pathlib import Path as KELIAS
operacinė_sistema_VALUE.path.insert(0, str(KELIAS(__file__).resolve().parents[1] / 'Įrankiai'))
if __name__ == '__main__':
    import runpy as programa_programų_skydelis
    programa_programų_skydelis.run_module('셸시험', run_name='__main__', alter_sys=True)
else:
    구현 = TAKE_VALUE.import_module('셸시험')
    susiejimas_VALUE = {'timeout': '시간제한', 'x': 'x_koordinatė', 'msg': 'tinklas_žinutė', 'i': '순번', 'reply': 'atsakyti', 'call': '호출', 'args': 'argumentas_ARRAY', 'chunk': '조각', 'data': 'duomenys', 'proc': 'Procesas', 'long_text': '긴글', 'restored': '복원자료', 'send': 'siųsti', 'file': 'Failas', 'main': 'Paleisti', 'found': 'Ieška_KR', 'ROOT': 'Project_šaknis', 'text': 'Tekstas', 'marker': 'žymeklis', 'command': 'Komanda', 'expected': '예상결과', 'pixel': 'pikselis', 'shell': 'apvalkalas', 'poll': '준비살피미', 'transcript': 'transkribavimas', 'end': 'baigti_pokalbį_OFFSET', 'image': 'IMAGE', 'key': '누름값', 'y': '세로좌표', 'output': 'išeiga', 'result': 'REZULTATAS', 'client': 'klientas', 'line': 'Eilutė', 'stream': 'Stream_VALUE', 'name': 'Pavadinimas_2', 'value': 'VALUE', 'receive': 'gauti_žinutė', 'report': 'tikrinimas_pranešti', 'work': '작업경로', 'qmp': '모의제어접속'}
    for 이전, dabartinis_prekė in susiejimas_VALUE.items():
        if hasattr(구현, dabartinis_prekė): globals()[이전] = getattr(구현, dabartinis_prekė)
