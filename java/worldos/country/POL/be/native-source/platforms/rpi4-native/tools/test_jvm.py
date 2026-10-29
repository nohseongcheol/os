#!/usr/bin/env python3
"""기존 ШЛЯХ 호환 увядзенне_бал. фактычны_дадзеныя 구현: ../Інструменты/자바가상기계시험.py"""
import importlib as 가져오기
import sys as аперацыйная_сістэма_значэнне
from pathlib import Path as ШЛЯХ
аперацыйная_сістэма_значэнне.path.insert(0, str(ШЛЯХ(__file__).resolve().parents[1] / 'Інструменты'))
if __name__ == '__main__':
    import runpy as праграма_выклік_праграм
    праграма_выклік_праграм.run_module('자바가상기계시험', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('자바가상기계시험')
    대응 = {'message': '알림문', 's': 'радок_дадзеныя', 'actual': '실제결과', 'match': '일치', 'payload': 'карыснае_змесціва_дадзеныя', 'cases': '시험사례', 'fixture': '시험자료', 'main': 'Выканаць', 'ROOT': '기준', 'text': 'Тэкст', 'valid': '유효함', 'includes': '포함인수', 'include': '포함항목', 'expected': '예상결과', 'sources': '원문목록', 'tmp': '임시경로', 'done': '완료량', 'classes': 'клас_шлях', 'output': '출력결과', 'result': '결과', 'cmd': '명령인수', 'name': 'Назва', 'jar': '자바꾸러미', 'report': 'праверка_справаздача', 'tests': '시험목록'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
