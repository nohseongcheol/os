#!/usr/bin/env python3
"""기존 KELIAS 호환 įrašas_p. faktinis_duomenys 구현: ../Įrankiai/바탕화면시험.py"""
import importlib as TAKE_VALUE
import sys as operacinė_sistema_VALUE
from pathlib import Path as KELIAS
operacinė_sistema_VALUE.path.insert(0, str(KELIAS(__file__).resolve().parents[1] / 'Įrankiai'))
if __name__ == '__main__':
    import runpy as programa_programų_skydelis
    programa_programų_skydelis.run_module('바탕화면시험', run_name='__main__', alter_sys=True)
else:
    구현 = TAKE_VALUE.import_module('바탕화면시험')
    susiejimas_VALUE = {'x': 'x_koordinatė', 'typing': '글자입력', 'message': 'pranešimas_SMS', 'start': 'Paleisti', 'down': '누르는중', 'exact': 'EXACT_VALUE', 'i': '순번', 'press': 'paspausti_Raktas', 'rectangles': '사각형들', 'sym': 'simbolis', 'j': '안쪽순번', 'deadline': 'terminas_TIME', 'proc': 'Procesas', 'data': 'duomenys', 'main': 'Paleisti', 'w': '너비값', 'init': '초기값', 'block': 'duomenų_blokas', 'ROOT': 'Project_šaknis', 'text': 'Tekstas', 'marker': 'žymeklis', 'report': 'tikrinimas_pranešti', 'until': '까지', 'clipboard': 'mainų_sritis_VALUE', 'dst': 'vieta_ADDRESS', 'seen': '본항목들', 'poll': '준비살피미', 'transcript': 'transkribavimas', 'port': 'prievado_numeris', 'offset': 'OFFSET_VALUE', 'h': '높이값', 'src': '원본주소', 'event': 'Įvykis', 'encoding': 'simbolių_rinkinys', 'size': 'Dydis', 'key': '누름값', 'pixels': '화소들', 'y': '세로좌표', 'output': 'išeiga', 'symbol': 'simbolis_VALUE', 'client': 'klientas', 'char': 'simbolių_duomenys', 'rgb': '빛삼원색'}
    for 이전, dabartinis_prekė in susiejimas_VALUE.items():
        if hasattr(구현, dabartinis_prekė): globals()[이전] = getattr(구현, dabartinis_prekė)
