#!/usr/bin/env python3
"""기존 Sti 호환 inngangspunkt. faktisk_data 구현: ../Verktøy/test_JVM.py"""
import importlib as TA_VERDI
import sys as operativsystem_VERDI
from pathlib import Path as Sti
operativsystem_VERDI.path.insert(0, str(Sti(__file__).resolve().parents[1] / 'Verktøy'))
if __name__ == '__main__':
    import runpy as app_appskuff
    app_appskuff.run_module('test_JVM', run_name='__main__', alter_sys=True)
else:
    구현 = TA_VERDI.import_module('test_JVM')
    tildeling_VERDI = {'message': 'notice_SMS', 's': 'streng_data', 'actual': 'faktisk_KR', 'match': '일치', 'payload': 'nyttelast_data', 'cases': 'test_sak', 'fixture': 'test_data', 'main': 'Kjør_2', 'ROOT': 'speile_rot', 'text': 'Tekst', 'valid': 'gyldig', 'includes': '포함인수', 'include': 'inkludere', 'expected': '예상결과', 'sources': '원문목록', 'tmp': '임시경로', 'done': 'Fullført_beløp', 'classes': 'time_bane', 'output': 'produksjon', 'result': 'KR', 'cmd': '명령인수', 'name': 'Navn', 'jar': '자바꾸러미', 'report': 'validering_rapport', 'tests': 'test_Liste'}
    for Forrige_vare, betalt_vare in tildeling_VERDI.items():
        if hasattr(구현, betalt_vare): globals()[Forrige_vare] = getattr(구현, betalt_vare)
