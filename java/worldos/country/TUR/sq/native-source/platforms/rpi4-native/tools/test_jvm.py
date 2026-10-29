#!/usr/bin/env python3
"""기존 POZICIONI 호환 futje_p. aktual_të_dhëna 구현: ../Mjete/자바가상기계시험.py"""
import importlib as TAKE_VALUE
import sys as sistem_operativ_VALUE
from pathlib import Path as POZICIONI
sistem_operativ_VALUE.path.insert(0, str(POZICIONI(__file__).resolve().parents[1] / 'Mjete'))
if __name__ == '__main__':
    import runpy as program_hapës
    program_hapës.run_module('자바가상기계시험', run_name='__main__', alter_sys=True)
else:
    구현 = TAKE_VALUE.import_module('자바가상기계시험')
    대응 = {'message': '알림문', 's': 'varg_të_dhëna', 'actual': 'aktual_llogaritje', 'match': '일치', 'payload': 'ngarkesë_e_dobishme_të_dhëna', 'cases': '시험사례', 'fixture': '시험자료', 'main': 'Ekzekuto', 'ROOT': 'Project_rrënjë', 'text': 'Teksti', 'valid': '유효함', 'includes': '포함인수', 'include': '포함항목', 'expected': '예상결과', 'sources': '원문목록', 'tmp': '임시경로', 'done': '완료량', 'classes': 'klasë_shteg', 'output': '출력결과', 'result': 'llogaritje', 'cmd': '명령인수', 'name': 'Emër', 'jar': '자바꾸러미', 'report': 'miratim_raport', 'tests': '시험목록'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
