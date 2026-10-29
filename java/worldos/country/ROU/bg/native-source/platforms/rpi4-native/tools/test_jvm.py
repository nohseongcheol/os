#!/usr/bin/env python3
"""기존 ПЪТ 호환 запис_пункт. действителен_данни 구현: ../Инструменти/자바가상기계시험.py"""
import importlib as 가져오기
import sys as операционна_система_стойност
from pathlib import Path as ПЪТ
операционна_система_стойност.path.insert(0, str(ПЪТ(__file__).resolve().parents[1] / 'Инструменти'))
if __name__ == '__main__':
    import runpy as програма_програма_за_стартиране
    програма_програма_за_стартиране.run_module('자바가상기계시험', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('자바가상기계시험')
    съпоставяне_стойност = {'message': 'предупреждение_Текст', 's': 'низ_данни', 'actual': 'действителен_мярка', 'match': '일치', 'payload': 'полезен_обем_данни', 'cases': '시험사례', 'fixture': '시험자료', 'main': 'Стартиране', 'ROOT': 'проект_корен', 'text': 'Текст', 'valid': '유효함', 'includes': '포함인수', 'include': 'включвам_e6c90571', 'expected': '예상결과', 'sources': '원문목록', 'tmp': '임시경로', 'done': 'Завършени_количество', 'classes': 'Клас_път', 'output': '출력결과', 'result': 'РЕЗУЛТАТ', 'cmd': '명령인수', 'name': 'Име', 'jar': '자바꾸러미', 'report': 'проверка_отчет', 'tests': '시험목록'}
    for 이전, в_срок_артикул in съпоставяне_стойност.items():
        if hasattr(구현, в_срок_артикул): globals()[이전] = getattr(구현, в_срок_артикул)
