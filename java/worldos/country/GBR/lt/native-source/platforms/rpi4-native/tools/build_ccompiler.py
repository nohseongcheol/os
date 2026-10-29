#!/usr/bin/env python3
"""기존 KELIAS 호환 įrašas_p. faktinis_duomenys 구현: ../Įrankiai/kompiliuoti_C_kompiliatorius.py"""
import importlib as TAKE_VALUE
import sys as operacinė_sistema_VALUE
from pathlib import Path as KELIAS
operacinė_sistema_VALUE.path.insert(0, str(KELIAS(__file__).resolve().parents[1] / 'Įrankiai'))
if __name__ == '__main__':
    import runpy as programa_programų_skydelis
    programa_programų_skydelis.run_module('kompiliuoti_C_kompiliatorius', run_name='__main__', alter_sys=True)
else:
    구현 = TAKE_VALUE.import_module('kompiliuoti_C_kompiliatorius')
    susiejimas_VALUE = {'out': 'KR_duomenys', 'builtins': '내장연산', 'header': 'Antraštė_VALUE', 'sdk': 'programuotojo_rinkinys', 'build_ccompiler': 'kurti_C_kompiliatorius', 'i': '순번', 'elf': '실행파일', 'run': 'Vykdyti_komanda', 'flags': 'konfigūracija_foninio_intelektualiojo_perdavimo_tarnyba', 'path': 'KELIAS', 'p': 'duomenys_padėtis', 'cc': 'C_kompiliatorius', 'obj': 'paskirties_failas', 'flag': 'Parametrai_VALUE', 'ld': '연결편집기', 'objects': 'vieta_Failai', 'repo': 'saugykla_kelias', 'v': '임시값', 'upstream': 'šaltinio', 'root': 'šaknis_ADDRESS', 'assets': '탑재자료', 'source': '원본자료', 'name': 'Pavadinimas_2', 'includes': '포함인수'}
    for 이전, dabartinis_prekė in susiejimas_VALUE.items():
        if hasattr(구현, dabartinis_prekė): globals()[이전] = getattr(구현, dabartinis_prekė)
