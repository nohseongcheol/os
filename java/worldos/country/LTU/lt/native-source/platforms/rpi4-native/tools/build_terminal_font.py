#!/usr/bin/env python3
"""기존 KELIAS 호환 įrašas_p. faktinis_duomenys 구현: ../Įrankiai/kompiliuoti_Terminalas_šriftas.py"""
import importlib as TAKE_VALUE
import sys as operacinė_sistema_VALUE
from pathlib import Path as KELIAS
operacinė_sistema_VALUE.path.insert(0, str(KELIAS(__file__).resolve().parents[1] / 'Įrankiai'))
if __name__ == '__main__':
    import runpy as programa_programų_skydelis
    programa_programų_skydelis.run_module('kompiliuoti_Terminalas_šriftas', run_name='__main__', alter_sys=True)
else:
    구현 = TAKE_VALUE.import_module('kompiliuoti_Terminalas_šriftas')
    susiejimas_VALUE = {'data': 'duomenys', 'img': 'piešinys_VALUE', 'bits': 'foninio_intelektualiojo_perdavimo_tarnyba_Sąrašas', 'x': 'x_koordinatė', 'draw': '화면그리기', 'licences': '이용허락목록', 'paths': 'kelias_Sąrašas', 'y': '세로좌표', 'main': 'Paleisti', 'src': '원본주소', 'fonts': 'šriftas_Sąrašas', 'ROOT': 'Project_šaknis', 'p': 'duomenys_padėtis', 'cp': 'simbolių_koduotė', 'target': 'tikslas'}
    for 이전, dabartinis_prekė in susiejimas_VALUE.items():
        if hasattr(구현, dabartinis_prekė): globals()[이전] = getattr(구현, dabartinis_prekė)
