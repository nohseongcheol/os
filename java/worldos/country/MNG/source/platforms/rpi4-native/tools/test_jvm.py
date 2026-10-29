#!/usr/bin/env python3
"""기존 ЗАМ 호환 оролт_цэг. бодит_өгөгдөл 구현: ../Хэрэгслүүд/자바가상기계시험.py"""
import importlib as 가져오기
import sys as үйлдлийн_систем_утга
from pathlib import Path as ЗАМ
үйлдлийн_систем_утга.path.insert(0, str(ЗАМ(__file__).resolve().parents[1] / 'Хэрэгслүүд'))
if __name__ == '__main__':
    import runpy as програм_гишүүн
    програм_гишүүн.run_module('자바가상기계시험', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('자바가상기계시험')
    대응 = {'message': '알림문', 's': 'мөр_өгөгдөл', 'actual': '실제결과', 'match': '일치', 'payload': 'ашигтай_ачаалал_өгөгдөл', 'cases': '시험사례', 'fixture': '시험자료', 'main': 'Ажиллуулах', 'ROOT': '기준', 'text': 'Бичвэр', 'valid': '유효함', 'includes': '포함인수', 'include': '포함항목', 'expected': '예상결과', 'sources': '원문목록', 'tmp': '임시경로', 'done': '완료량', 'classes': 'класс_зам', 'output': '출력결과', 'result': '결과', 'cmd': '명령인수', 'name': 'Нэр', 'jar': '자바꾸러미', 'report': 'баталгаажуулалт_тайлан', 'tests': '시험목록'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
