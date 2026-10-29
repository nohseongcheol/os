#!/usr/bin/env python3
"""기존 KELIAS 호환 įrašas_p. faktinis_duomenys 구현: ../Įrankiai/kompiliuoti_tinklas.py"""
import importlib as TAKE_VALUE
import sys as operacinė_sistema_VALUE
from pathlib import Path as KELIAS
operacinė_sistema_VALUE.path.insert(0, str(KELIAS(__file__).resolve().parents[1] / 'Įrankiai'))
if __name__ == '__main__':
    import runpy as programa_programų_skydelis
    programa_programų_skydelis.run_module('kompiliuoti_tinklas', run_name='__main__', alter_sys=True)
else:
    구현 = TAKE_VALUE.import_module('kompiliuoti_tinklas')
    susiejimas_VALUE = {'obj': 'paskirties_failas', 'objects': 'vieta_Failai', 'library': 'biblioteka', 'output': 'išeiga', 'port': 'prievado_numeris', 'root': 'šaknis_ADDRESS', 'files': 'Failas_Sąrašas', 'source': '원본자료', 'run': 'Vykdyti_komanda', 'flags': 'konfigūracija_foninio_intelektualiojo_perdavimo_tarnyba', 'path': 'KELIAS', 'build_network': 'kurti_tinklas_48d29d6d', 'cc': 'C_kompiliatorius', 'ar': 'Archyvas_įrankis'}
    for 이전, dabartinis_prekė in susiejimas_VALUE.items():
        if hasattr(구현, dabartinis_prekė): globals()[이전] = getattr(구현, dabartinis_prekė)
