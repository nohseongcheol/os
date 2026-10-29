#!/usr/bin/env python3
"""기존 ПАТЕКА 호환 внес_поен. реален_податоци 구현: ../Алатки/자바가상기계시험.py"""
import importlib as TAKE_VALUE
import sys as оперативен_систем_VALUE
from pathlib import Path as ПАТЕКА
оперативен_систем_VALUE.path.insert(0, str(ПАТЕКА(__file__).resolve().parents[1] / 'Алатки'))
if __name__ == '__main__':
    import runpy as програма_стартувач
    програма_стартувач.run_module('자바가상기계시험', run_name='__main__', alter_sys=True)
else:
    구현 = TAKE_VALUE.import_module('자바가상기계시험')
    대응 = {'message': '알림문', 's': 'низа_податоци', 'actual': 'реален_мерка', 'match': '일치', 'payload': 'капацитет_податоци', 'cases': '시험사례', 'fixture': '시험자료', 'main': 'Изврши_2', 'ROOT': 'Project_корен', 'text': 'Текст', 'valid': '유효함', 'includes': '포함인수', 'include': '포함항목', 'expected': '예상결과', 'sources': '원문목록', 'tmp': '임시경로', 'done': '완료량', 'classes': 'класа_патека', 'output': '출력결과', 'result': 'мерка', 'cmd': '명령인수', 'name': 'Име', 'jar': '자바꾸러미', 'report': 'проверка_извештај', 'tests': '시험목록'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
