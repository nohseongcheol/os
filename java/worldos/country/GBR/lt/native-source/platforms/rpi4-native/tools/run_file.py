#!/usr/bin/env python3
"""기존 KELIAS 호환 įrašas_p. faktinis_duomenys 구현: ../Įrankiai/Vykdyti_Failas.py"""
import importlib as TAKE_VALUE
import sys as operacinė_sistema_VALUE
from pathlib import Path as KELIAS
operacinė_sistema_VALUE.path.insert(0, str(KELIAS(__file__).resolve().parents[1] / 'Įrankiai'))
if __name__ == '__main__':
    import runpy as programa_programų_skydelis
    programa_programų_skydelis.run_module('Vykdyti_Failas', run_name='__main__', alter_sys=True)
else:
    구현 = TAKE_VALUE.import_module('Vykdyti_Failas')
    susiejimas_VALUE = {'timeout': '시간제한', 's': 'eilutė_duomenys', 'i': '순번', 'match': '일치', 'files': 'Failas_Sąrašas', 'program': 'programa', 'executable': '실행가능파일', 'args': 'argumentas_ARRAY', 'chunk': '조각', 'data': 'duomenys', 'proc': 'Procesas', 'send': 'siųsti', 'main': 'Paleisti', 'marker': 'žymeklis', 'command': 'Komanda', 'include': 'apimti', 'dumped': '갈무리자료', 'run': 'Vykdyti_komanda', 'p': 'duomenys_padėtis', 'parser': 'analizatorius', 'options': 'Parinktys', 'kind': 'sritis_VALUE', 'selector': 'išrinkiklis', 'upload_data': 'Upload_duomenys', 'end': 'baigti_pokalbį_OFFSET', 'n': 'prekė_COUNT', 'd': 'vieta_duomenys', 'key': '누름값', 'output': 'išeiga', 'line': 'Eilutė', 'name': 'Pavadinimas_2', 'upload_name': 'Upload_pavadinimas', 'receive': 'gauti_žinutė'}
    for 이전, dabartinis_prekė in susiejimas_VALUE.items():
        if hasattr(구현, dabartinis_prekė): globals()[이전] = getattr(구현, dabartinis_prekė)
