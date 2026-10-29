#!/usr/bin/env python3
"""기존 шлях 호환 запис_бал. фактично_дані реалізація: ../інструменти/자바가상기계시험.py"""
import importlib as 가져오기
import sys as операційна_система_ОС_значення
from pathlib import Path as шлях
операційна_система_ОС_значення.path.insert(0, str(шлях(__file__).resolve().parents[1] / 'інструменти'))
if __name__ == '__main__':
    import runpy as програма_запускач
    програма_запускач.run_module('자바가상기계시험', run_name='__main__', alter_sys=True)
else:
    реалізація = 가져오기.import_module('자바가상기계시험')
    зіставлення_значення = {'message': 'повідомлення_Текст', 's': 'рядок_дані', 'actual': 'фактично_КР', 'match': '일치', 'payload': 'вміст_пакета_дані', 'cases': '시험사례', 'fixture': '시험자료', 'main': 'запустити', 'ROOT': 'Дії_корінь', 'text': 'текст', 'valid': '유효함', 'includes': '포함인수', 'include': 'містити', 'expected': '예상결과', 'sources': '원문목록', 'tmp': '임시경로', 'done': 'Виконано_сума', 'classes': 'Клас_шлях', 'output': '출력결과', 'result': 'результат', 'cmd': '명령인수', 'name': 'Назва', 'jar': '자바꾸러미', 'report': 'перевірка_звіт', 'tests': '시험목록'}
    for 이전, чинний_елемент in зіставлення_значення.items():
        if hasattr(реалізація, чинний_елемент): globals()[이전] = getattr(реалізація, чинний_елемент)
