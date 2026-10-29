#!/usr/bin/env python3
"""기존 pad 호환 beginpunt. werkelijk_gegevens implementatie: ../hulpmiddelen/test_JVM.py"""
import importlib as NEMEN_WAARDE
import sys as besturingssysteem_WAARDE
from pathlib import Path as pad
besturingssysteem_WAARDE.path.insert(0, str(pad(__file__).resolve().parents[1] / 'hulpmiddelen'))
if __name__ == '__main__':
    import runpy as app_app_lade
    app_app_lade.run_module('test_JVM', run_name='__main__', alter_sys=True)
else:
    implementatie = NEMEN_WAARDE.import_module('test_JVM')
    toewijzing_WAARDE = {'message': 'kennisgeving_sms', 's': 'tekenreeks_gegevens', 'actual': 'werkelijk_HR', 'match': '일치', 'payload': 'payload_gegevens', 'cases': 'test_case', 'fixture': 'test_gegevens', 'main': 'starten', 'ROOT': 'Taken_wortel', 'text': 'tekst', 'valid': 'geldig', 'includes': '포함인수', 'include': 'bevatten', 'expected': '예상결과', 'sources': '원문목록', 'tmp': '임시경로', 'done': 'Voltooid_aantal', 'classes': 'les_pad', 'output': 'uitvoer', 'result': 'resultaat', 'cmd': '명령인수', 'name': 'Naam', 'jar': '자바꾸러미', 'report': 'validatie_Rapport', 'tests': 'test_Lijst'}
    for Vorige_item, actueel_item in toewijzing_WAARDE.items():
        if hasattr(implementatie, actueel_item): globals()[Vorige_item] = getattr(implementatie, actueel_item)
