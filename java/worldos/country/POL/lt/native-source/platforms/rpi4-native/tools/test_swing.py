#!/usr/bin/env python3
"""기존 KELIAS 호환 įrašas_p. faktinis_duomenys 구현: ../Įrankiai/화면요소시험.py"""
import importlib as TAKE_VALUE
import sys as operacinė_sistema_VALUE
from pathlib import Path as KELIAS
operacinė_sistema_VALUE.path.insert(0, str(KELIAS(__file__).resolve().parents[1] / 'Įrankiai'))
if __name__ == '__main__':
    import runpy as programa_programų_skydelis
    programa_programų_skydelis.run_module('화면요소시험', run_name='__main__', alter_sys=True)
else:
    구현 = TAKE_VALUE.import_module('화면요소시험')
    susiejimas_VALUE = {'wait': '기다리기', 'x': 'x_koordinatė', 's': 'eilutė_duomenys', 'i': '순번', 'sel': 'išrinkiklis_a916db4e', 'seconds': '초단위', 'log': 'LOG_RECORD', 'data': 'duomenys', 'at': 'dabartinis_padėtis', 'send': 'siųsti', 'main': 'Paleisti', 'req': 'užklausa_VALUE_625fa62c', 'hot': 'nuoroda_VALUE', 'pump': 'rodyklė_įvykis', 'ROOT': 'Project_šaknis', 'marker': 'žymeklis', 'b': 'SECOND_VALUE', 'command': 'Komanda', 'shell': 'apvalkalas', 'f': 'Failas_įrašas', 'click': 'spustelėti_mygtukas', 'k': '셋째순번', 'c': 'simbolio_kodas', 'r': '반환값', 'p': 'duomenys_padėtis', 'command_mode': 'komanda_MODE', 'end': 'baigti_pokalbį_OFFSET', 'classes': 'klasė_kelias', 'key': '누름값', 'y': '세로좌표', 'result': 'REZULTATAS', 'report': 'tikrinimas_pranešti', 'dest': 'vieta_VALUE_padėtis', 'work': '작업경로', 'qmp': '모의제어접속'}
    for 이전, dabartinis_prekė in susiejimas_VALUE.items():
        if hasattr(구현, dabartinis_prekė): globals()[이전] = getattr(구현, dabartinis_prekė)
