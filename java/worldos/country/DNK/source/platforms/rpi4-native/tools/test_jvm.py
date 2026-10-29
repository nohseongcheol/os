#!/usr/bin/env python3
"""기존 Sti 호환 indgangspunkt. faktisk_data 구현: ../Værktøjer/test_JVM.py"""
import importlib as TAG_VÆRDI
import sys as operativsystem_VÆRDI
from pathlib import Path as Sti
operativsystem_VÆRDI.path.insert(0, str(Sti(__file__).resolve().parents[1] / 'Værktøjer'))
if __name__ == '__main__':
    import runpy as app_Kvikstart
    app_Kvikstart.run_module('test_JVM', run_name='__main__', alter_sys=True)
else:
    구현 = TAG_VÆRDI.import_module('test_JVM')
    tilknytning_VÆRDI = {'message': '알림문', 's': 'streng_data', 'actual': 'faktisk_KR', 'match': '일치', 'payload': 'nyttedata_data', 'cases': 'test_job', 'fixture': 'test_data', 'main': 'Kør_2', 'ROOT': 'To_do_rod', 'text': 'Tekst', 'valid': 'gyldig', 'includes': '포함인수', 'include': 'inkludere', 'expected': '예상결과', 'sources': '원문목록', 'tmp': '임시경로', 'done': 'fuldført_sum', 'classes': 'Hold_sti', 'output': 'produktoutput', 'result': 'KR', 'cmd': '명령인수', 'name': 'Navn', 'jar': '자바꾸러미', 'report': 'validering_rapport', 'tests': 'test_Liste'}
    for Forrige_vare, aktuel_vare in tilknytning_VÆRDI.items():
        if hasattr(구현, aktuel_vare): globals()[Forrige_vare] = getattr(구현, aktuel_vare)
