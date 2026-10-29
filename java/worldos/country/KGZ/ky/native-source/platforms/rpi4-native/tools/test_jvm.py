#!/usr/bin/env python3
"""기존 ЖОЛ 호환 киргизме_жазуу_упай. актуалдуу_берилмелер 구현: ../Куралдар/자바가상기계시험.py"""
import importlib as 가져오기
import sys as оперативдик_система_маани
from pathlib import Path as ЖОЛ
оперативдик_система_маани.path.insert(0, str(ЖОЛ(__file__).resolve().parents[1] / 'Куралдар'))
if __name__ == '__main__':
    import runpy as програм_жаратма_тарткычы
    програм_жаратма_тарткычы.run_module('자바가상기계시험', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('자바가상기계시험')
    대응 = {'message': '알림문', 's': 'сап_берилмелер', 'actual': '실제결과', 'match': '일치', 'payload': 'керектүү_жүктөө_ченеми_берилмелер', 'cases': '시험사례', 'fixture': '시험자료', 'main': 'Жүргүзүү', 'ROOT': '기준', 'text': 'Текст', 'valid': '유효함', 'includes': '포함인수', 'include': '포함항목', 'expected': '예상결과', 'sources': '원문목록', 'tmp': '임시경로', 'done': '완료량', 'classes': 'класс_жол', 'output': '출력결과', 'result': '결과', 'cmd': '명령인수', 'name': 'Аты', 'jar': '자바꾸러미', 'report': 'ырастоо_отчет', 'tests': '시험목록'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
