#!/usr/bin/env python3
"""기존 يول 호환 كىرگۈزۈش_نوقتا. ھەقىقىي_مەلۇمات 구현: ../قوراللار/자바가상기계시험.py"""
import importlib as 가져오기
import sys as مەشغۇلات_سىستېمىسى_قىممىتى
from pathlib import Path as يول
مەشغۇلات_سىستېمىسى_قىممىتى.path.insert(0, str(يول(__file__).resolve().parents[1] / 'قوراللار'))
if __name__ == '__main__':
    import runpy as ئەپ_خادىم
    ئەپ_خادىم.run_module('자바가상기계시험', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('자바가상기계시험')
    대응 = {'message': '알림문', 's': 'ھەرپ_تىزمىسى_مەلۇمات', 'actual': 'ھەقىقىي_ئۆلچەم', 'match': '일치', 'payload': 'يۈك_مەلۇمات', 'cases': '시험사례', 'fixture': '시험자료', 'main': 'ئىجرا_قىل_2', 'ROOT': 'كۆرسىتىش_يىلتىز', 'text': 'تېكىست', 'valid': '유효함', 'includes': '포함인수', 'include': '포함항목', 'expected': '예상결과', 'sources': '원문목록', 'tmp': '임시경로', 'done': '완료량', 'classes': 'تۈركۈم_يول', 'output': '출력결과', 'result': 'ئۆلچەم', 'cmd': '명령인수', 'name': 'ئاتى', 'jar': '자바꾸러미', 'report': 'دەلىللەش_خەۋەر', 'tests': '시험목록'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
