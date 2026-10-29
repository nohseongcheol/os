#!/usr/bin/env python3
"""기존 પથ 호환 પ્રવેશ_બિંદુ. વાસ્તવિક_ડેટા 구현: ../ઉપકરણો/અપલોડ_કરો_ફાઇલો.py"""
import importlib as 가져오기
import sys as ઑપરેટિંગ_સિસ્ટમ_મૂલ્ય
from pathlib import Path as પથ
ઑપરેટિંગ_સિસ્ટમ_મૂલ્ય.path.insert(0, str(પથ(__file__).resolve().parents[1] / 'ઉપકરણો'))
if __name__ == '__main__':
    import runpy as એપ્લિકેશન_લૉન્ચર
    એપ્લિકેશન_લૉન્ચર.run_module('અપલોડ_કરો_ફાઇલો', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('અપલોડ_કરો_ફાઇલો')
    대응 = {'data': 'ડેટા', 'i': '순번', 'name': 'નામ', 'c': 'વર્ણ_કોડ', 'p': 'ડેટા_સ્થિતિ', 'args': 'દલીલ_અરે'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
