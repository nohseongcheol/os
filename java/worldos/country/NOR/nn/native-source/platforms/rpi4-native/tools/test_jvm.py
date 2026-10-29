#!/usr/bin/env python3
"""기존 STIGE 호환 oppføring_p. faktisk_data 구현: ../Verktøy/자바가상기계시험.py"""
import importlib as TAKE_VALUE
import sys as operativsystem_VALUE
from pathlib import Path as STIGE
operativsystem_VALUE.path.insert(0, str(STIGE(__file__).resolve().parents[1] / 'Verktøy'))
if __name__ == '__main__':
    import runpy as app_appskuff
    app_appskuff.run_module('자바가상기계시험', run_name='__main__', alter_sys=True)
else:
    구현 = TAKE_VALUE.import_module('자바가상기계시험')
    대응 = {'message': '알림문', 's': 'streng_data', 'actual': 'faktisk_forretningsmål', 'match': '일치', 'payload': 'nyttelast_data', 'cases': '시험사례', 'fixture': '시험자료', 'main': 'Køyr_2', 'ROOT': 'spegle_rot', 'text': 'Tekst', 'valid': '유효함', 'includes': '포함인수', 'include': '포함항목', 'expected': '예상결과', 'sources': '원문목록', 'tmp': '임시경로', 'done': '완료량', 'classes': 'time_bane', 'output': '출력결과', 'result': 'forretningsmål', 'cmd': '명령인수', 'name': 'Namn', 'jar': '자바꾸러미', 'report': 'validering_rapport', 'tests': '시험목록'}
    for 이전, betalt_vare in 대응.items():
        if hasattr(구현, betalt_vare): globals()[이전] = getattr(구현, betalt_vare)
