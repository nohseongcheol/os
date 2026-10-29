#!/usr/bin/env python3
"""기존 KELIAS 호환 įrašas_p. faktinis_duomenys 구현: ../Įrankiai/eksportuoti_SDK.py"""
import importlib as TAKE_VALUE
import sys as operacinė_sistema_VALUE
from pathlib import Path as KELIAS
operacinė_sistema_VALUE.path.insert(0, str(KELIAS(__file__).resolve().parents[1] / 'Įrankiai'))
if __name__ == '__main__':
    import runpy as programa_programų_skydelis
    programa_programų_skydelis.run_module('eksportuoti_SDK', run_name='__main__', alter_sys=True)
else:
    구현 = TAKE_VALUE.import_module('eksportuoti_SDK')
    susiejimas_VALUE = {'out': 'KR_duomenys', 'obj': 'paskirties_failas', 'relative': 'santykinis_kelias', 'compiler_archive': 'kompiliatorius_Archyvas', 'sdk': 'programuotojo_rinkinys', 'dist': 'paskirstymas_kelias', 'archive': 'Archyvas', 'main': 'Paleisti', 'posix': '포직스경로', 'files': 'Failas_Sąrašas', 'source': '원본자료', 'name': 'Pavadinimas_2', 'target': 'tikslas', 'ROOT': 'Project_šaknis', 'destination': 'vieta_duomenys_ADDRESS', 'manifest': '꾸러미명세', 'work': '작업경로'}
    for 이전, dabartinis_prekė in susiejimas_VALUE.items():
        if hasattr(구현, dabartinis_prekė): globals()[이전] = getattr(구현, dabartinis_prekė)
