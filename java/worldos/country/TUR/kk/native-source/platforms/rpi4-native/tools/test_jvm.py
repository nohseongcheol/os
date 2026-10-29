#!/usr/bin/env python3
"""기존 Жол_2 호환 енгізу_ұпай. нақты_деректер 구현: ../Құралдар/자바가상기계시험.py"""
import importlib as 가져오기
import sys as операциялық_жүйе_мән
from pathlib import Path as Жол_2
операциялық_жүйе_мән.path.insert(0, str(Жол_2(__file__).resolve().parents[1] / 'Құралдар'))
if __name__ == '__main__':
    import runpy as бағдарлама_іске_қосу_құралы
    бағдарлама_іске_қосу_құралы.run_module('자바가상기계시험', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('자바가상기계시험')
    대응 = {'message': '알림문', 's': 'жол_деректер', 'actual': 'нақты_өлшем', 'match': '일치', 'payload': 'жүктеме_деректер', 'cases': '시험사례', 'fixture': '시험자료', 'main': 'Орындау_2', 'ROOT': 'жоба_түбір', 'text': 'Мәтін', 'valid': '유효함', 'includes': '포함인수', 'include': '포함항목', 'expected': '예상결과', 'sources': '원문목록', 'tmp': '임시경로', 'done': 'Орындалғандар_көлем', 'classes': 'оқу_жол', 'output': '출력결과', 'result': 'НӘТИЖЕ', 'cmd': '명령인수', 'name': 'Аты', 'jar': '자바꾸러미', 'report': 'тексерім_есеп', 'tests': '시험목록'}
    for 이전, ток_элемент in 대응.items():
        if hasattr(구현, ток_элемент): globals()[이전] = getattr(구현, ток_элемент)
