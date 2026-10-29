#!/usr/bin/env python3
"""기존 પથ 호환 પ્રવેશ_બિંદુ. વાસ્તવિક_ડેટા 구현: ../ઉપકરણો/실행파일시험.py"""
import importlib as 가져오기
import sys as ઑપરેટિંગ_સિસ્ટમ_મૂલ્ય
from pathlib import Path as પથ
ઑપરેટિંગ_સિસ્ટમ_મૂલ્ય.path.insert(0, str(પથ(__file__).resolve().parents[1] / 'ઉપકરણો'))
if __name__ == '__main__':
    import runpy as એપ્લિકેશન_લૉન્ચર
    એપ્લિકેશન_લૉન્ચર.run_module('실행파일시험', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('실행파일시험')
    대응 = {'out': 'પરિમાણ_ડેટા', 'expected': '예상결과', 'phoff': 'એપ્લિકેશન_શીર્ષલેખ_ઑફસેટ', 'offset': 'ઑફસેટ_મૂલ્ય', 'invalid': 'અમાન્ય_ડેટા', 'path': 'પથ', 'executable': '실행가능파일', 'rejected': '거부결과', 'linux_example': '리눅스예제', 'original': '원본', 'result': 'પરિમાણ', 'format_': 'સ્વરૂપ_b87fd068', 'main': 'ચલાવો_2', 'content': 'સામગ્રી_મૂલ્ય', 'source': '원본자료', 'name': 'નામ', 'reference': '비교기준', 'ROOT': 'પ્રોજેક્ટ_રૂટ', 'value': 'મૂલ્ય', 'report': 'માન્યતા_અહેવાલ'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
