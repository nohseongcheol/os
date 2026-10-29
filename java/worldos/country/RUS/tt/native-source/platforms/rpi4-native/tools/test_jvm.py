#!/usr/bin/env python3
"""기존 Yul 호환 кертү_балл. фактик_мәгълүмат 구현: ../Кораллар/자바가상기계시험.py"""
import importlib as TAKE_VALUE
import sys as операцион_система_VALUE
from pathlib import Path as Yul
операцион_система_VALUE.path.insert(0, str(Yul(__file__).resolve().parents[1] / 'Кораллар'))
if __name__ == '__main__':
    import runpy as кушымта_хезмәткәр
    кушымта_хезмәткәр.run_module('자바가상기계시험', run_name='__main__', alter_sys=True)
else:
    구현 = TAKE_VALUE.import_module('자바가상기계시험')
    대응 = {'message': '알림문', 's': 'юл_мәгълүмат', 'actual': 'фактик_үлчәм', 'match': '일치', 'payload': 'төп_өлеш_мәгълүмат', 'cases': '시험사례', 'fixture': '시험자료', 'main': 'эшләтү', 'ROOT': 'экранга_җибәрү_тамыр', 'text': 'Mäten', 'valid': '유효함', 'includes': '포함인수', 'include': '포함항목', 'expected': '예상결과', 'sources': '원문목록', 'tmp': '임시경로', 'done': '완료량', 'classes': 'класс_юл', 'output': '출력결과', 'result': 'үлчәм', 'cmd': '명령인수', 'name': 'исем', 'jar': '자바꾸러미', 'report': 'раслау_отчет', 'tests': '시험목록'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
