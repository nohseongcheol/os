#!/usr/bin/env python3
"""기존 KELIAS 호환 įrašas_p. faktinis_duomenys 구현: ../Įrankiai/kompiliuoti_PYTHON.py"""
import importlib as TAKE_VALUE
import sys as operacinė_sistema_VALUE
from pathlib import Path as KELIAS
operacinė_sistema_VALUE.path.insert(0, str(KELIAS(__file__).resolve().parents[1] / 'Įrankiai'))
if __name__ == '__main__':
    import runpy as programa_programų_skydelis
    programa_programų_skydelis.run_module('kompiliuoti_PYTHON', run_name='__main__', alter_sys=True)
else:
    구현 = TAKE_VALUE.import_module('kompiliuoti_PYTHON')
    susiejimas_VALUE = {'ld': '연결편집기', 'archive': 'Archyvas', 'SHA256': 'tikrinimas_maiša', 'build_python': 'kurti_PYTHON', 'root': 'šaknis_ADDRESS', 'source': '원본자료', 'name': 'Pavadinimas_2', 'path': 'KELIAS', 'VERSION': 'leidimas_VALUE', 'cc': 'C_kompiliatorius', 'tar': '타르꾸러미', 'newlib': '뉴리브포함경로', 'member': 'narys'}
    for 이전, dabartinis_prekė in susiejimas_VALUE.items():
        if hasattr(구현, dabartinis_prekė): globals()[이전] = getattr(구현, dabartinis_prekė)
