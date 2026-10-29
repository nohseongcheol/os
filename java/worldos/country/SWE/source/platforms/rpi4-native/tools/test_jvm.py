#!/usr/bin/env python3
"""기존 sökväg_2 호환 startpunkt. verklig_data implementation: ../verktyg/test_JVM.py"""
import importlib as TA_värde
import sys as operativsystem_värde
from pathlib import Path as sökväg_2
operativsystem_värde.path.insert(0, str(sökväg_2(__file__).resolve().parents[1] / 'verktyg'))
if __name__ == '__main__':
    import runpy as app_Startbild
    app_Startbild.run_module('test_JVM', run_name='__main__', alter_sys=True)
else:
    implementation = TA_värde.import_module('test_JVM')
    mappning_värde = {'message': '알림문', 's': 'sträng_data', 'actual': 'verklig_KR', 'match': '일치', 'payload': 'nyttolast_data', 'cases': 'test_akt', 'fixture': 'test_data', 'main': 'Kör', 'ROOT': 'åtgärd_rot', 'text': 'text', 'valid': 'giltig', 'includes': '포함인수', 'include': 'ta_med', 'expected': '예상결과', 'sources': '원문목록', 'tmp': '임시경로', 'done': 'Slutfört_belopp', 'classes': 'Kurs_väg', 'output': 'utleverans', 'result': 'RESULTAT', 'cmd': '명령인수', 'name': 'Namn', 'jar': '자바꾸러미', 'report': 'validering_Rapport', 'tests': 'test_ange'}
    for Föregående_objekt, aktuellt_objekt in mappning_värde.items():
        if hasattr(implementation, aktuellt_objekt): globals()[Föregående_objekt] = getattr(implementation, aktuellt_objekt)
