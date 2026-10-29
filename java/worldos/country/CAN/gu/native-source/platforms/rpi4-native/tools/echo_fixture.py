#!/usr/bin/env python3
"""기존 પથ 호환 પ્રવેશ_બિંદુ. વાસ્તવિક_ડેટા 구현: ../ઉપકરણો/되돌림시험서버.py"""
import importlib as 가져오기
import sys as ઑપરેટિંગ_સિસ્ટમ_મૂલ્ય
from pathlib import Path as પથ
ઑપરેટિંગ_સિસ્ટમ_મૂલ્ય.path.insert(0, str(પથ(__file__).resolve().parents[1] / 'ઉપકરણો'))
if __name__ == '__main__':
    import runpy as એપ્લિકેશન_લૉન્ચર
    એપ્લિકેશન_લૉન્ચર.run_module('되돌림시험서버', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('되돌림시험서버')
    대응 = {'data': 'ડેટા', 'e': '보조항목', 'connection': 'કનેક્શન_e05f319b', 'f': 'ફાઇલ_પ્રવેશ', 'peer': 'પીઅર_મૂલ્ય', 'self': '자신', 'udp': '전문제어', 't': 'ટર્મિનલ_પ્રવેશ', 'tcp': 'કનેક્શન_નિયંત્રણ', 'EchoFixture': '되돌림시험서버', 'args': 'દલીલ_અરે', 'chunk': '조각'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
