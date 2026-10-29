#!/usr/bin/env python3
"""기존 пут 호환 унос_тачка. стваран_подаци 구현: ../도구/자바가상기계시험.py"""
import importlib as 가져오기
import sys as оперативни_систем_вриједност
from pathlib import Path as пут
оперативни_систем_вриједност.path.insert(0, str(пут(__file__).resolve().parents[1] / '도구'))
if __name__ == '__main__':
    import runpy as 실행기
    실행기.run_module('자바가상기계시험', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('자바가상기계시험')
    대응 = {'message': '알림문', 's': 'стринг_подаци', 'actual': '실제결과', 'match': '일치', 'payload': 'корисни_садржај_подаци', 'cases': '시험사례', 'fixture': '시험자료', 'main': '시작', 'ROOT': '기준', 'text': 'текст', 'valid': '유효함', 'includes': '포함인수', 'include': '포함항목', 'expected': '예상결과', 'sources': '원문목록', 'tmp': '임시경로', 'done': '완료량', 'classes': 'класа_пут', 'output': '출력결과', 'result': '결과', 'cmd': '명령인수', 'name': 'назив', 'jar': '자바꾸러미', 'report': 'провјера_извјештај', 'tests': '시험목록'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
