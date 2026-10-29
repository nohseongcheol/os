#!/usr/bin/env python3
"""기존 Pad 호환 inskrywing_p. werklik_data 구현: ../Nutsmiddels/자바가상기계시험.py"""
import importlib as TAKE_VALUE
import sys as bedryfstelsel_VALUE
from pathlib import Path as Pad
bedryfstelsel_VALUE.path.insert(0, str(Pad(__file__).resolve().parents[1] / 'Nutsmiddels'))
if __name__ == '__main__':
    import runpy as program_oopmaker
    program_oopmaker.run_module('자바가상기계시험', run_name='__main__', alter_sys=True)
else:
    구현 = TAKE_VALUE.import_module('자바가상기계시험')
    대응 = {'message': '알림문', 's': 'string_data', 'actual': 'werklik_maatreël', 'match': '일치', 'payload': 'lading_data', 'cases': '시험사례', 'fixture': '시험자료', 'main': 'Loop', 'ROOT': 'Project_wortel', 'text': 'Teks', 'valid': '유효함', 'includes': '포함인수', 'include': '포함항목', 'expected': '예상결과', 'sources': '원문목록', 'tmp': '임시경로', 'done': '완료량', 'classes': 'Klas_pad', 'output': '출력결과', 'result': 'maatreël', 'cmd': '명령인수', 'name': 'Naam', 'jar': '자바꾸러미', 'report': 'validering_verslag', 'tests': '시험목록'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
