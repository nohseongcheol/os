#!/usr/bin/env python3
"""기존 પથ 호환 પ્રવેશ_બિંદુ. વાસ્તવિક_ડેટા 구현: ../ઉપકરણો/자바가상기계시험.py"""
import importlib as 가져오기
import sys as ઑપરેટિંગ_સિસ્ટમ_મૂલ્ય
from pathlib import Path as પથ
ઑપરેટિંગ_સિસ્ટમ_મૂલ્ય.path.insert(0, str(પથ(__file__).resolve().parents[1] / 'ઉપકરણો'))
if __name__ == '__main__':
    import runpy as એપ્લિકેશન_લૉન્ચર
    એપ્લિકેશન_લૉન્ચર.run_module('자바가상기계시험', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('자바가상기계시험')
    대응 = {'message': '알림문', 's': 'સ્ટ્રિંગ_ડેટા', 'actual': 'વાસ્તવિક_પરિમાણ', 'match': '일치', 'payload': 'પેલોડ_ડેટા', 'cases': '시험사례', 'fixture': '시험자료', 'main': 'ચલાવો_2', 'ROOT': 'પ્રોજેક્ટ_રૂટ', 'text': 'લખાણ', 'valid': '유효함', 'includes': '포함인수', 'include': '포함항목', 'expected': '예상결과', 'sources': '원문목록', 'tmp': '임시경로', 'done': '완료량', 'classes': 'વર્ગ_પાથ', 'output': '출력결과', 'result': 'પરિમાણ', 'cmd': '명령인수', 'name': 'નામ', 'jar': '자바꾸러미', 'report': 'માન્યતા_અહેવાલ', 'tests': '시험목록'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
