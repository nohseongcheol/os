#!/usr/bin/env python3
"""기존 KELIAS 호환 įrašas_p. faktinis_duomenys 구현: ../Įrankiai/kompiliuoti_sistema.py"""
import importlib as TAKE_VALUE
import sys as operacinė_sistema_VALUE
from pathlib import Path as KELIAS
operacinė_sistema_VALUE.path.insert(0, str(KELIAS(__file__).resolve().parents[1] / 'Įrankiai'))
if __name__ == '__main__':
    import runpy as programa_programų_skydelis
    programa_programų_skydelis.run_module('kompiliuoti_sistema', run_name='__main__', alter_sys=True)
else:
    구현 = TAKE_VALUE.import_module('kompiliuoti_sistema')
    susiejimas_VALUE = {'network': 'tinklas', 'BUILD': 'kompiliuoti_kelias', 'ar': 'Archyvas_įrankis', 'build_examples': '예제만들기', 'posix': '포직스경로', 'font_data': 'šriftas_duomenys', 'flags': 'konfigūracija_foninio_intelektualiojo_perdavimo_tarnyba', 'a': '첫째값', 'cc': 'C_kompiliatorius', 'args': 'argumentas_ARRAY', 'source_flags': '원본설정', 'ld': '연결편집기', 'method': 'metodas_įrašas', 'main': 'Paleisti', 'objcopy': 'objektas_Failas_keitiklis', 'ROOT': 'Project_šaknis', 'cxx': '시플플번역기', 'includes': '포함인수', 'compiler': 'kompiliatorius_įrankis', 'build_users': 'kurti_naudotojas_erdvė', 'f': 'Failas_įrašas', 'extra': '추가영역', 'exports': 'eksportuoti_lentelė', 'jobs': '빌드작업', 'run': 'Vykdyti_komanda', 'path': 'KELIAS', 'REPO': 'saugykla_šaknis', 'tool': 'Įrankiai', 'classes': 'klasė_kelias', 'output': 'išeiga', 'samples': '예제들', 'symbol': 'simbolis_VALUE', 'source': '원본자료', 'name': 'Pavadinimas_2', 'build_network': 'kurti_tinklas_48d29d6d', 'font_info': 'šriftas_informacija', 'manifest': '꾸러미명세', 'work': '작업경로'}
    for 이전, dabartinis_prekė in susiejimas_VALUE.items():
        if hasattr(구현, dabartinis_prekė): globals()[이전] = getattr(구현, dabartinis_prekė)
