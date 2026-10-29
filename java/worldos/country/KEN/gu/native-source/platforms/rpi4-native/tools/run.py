#!/usr/bin/env python3
"""기존 પથ 호환 પ્રવેશ_બિંદુ. વાસ્તવિક_ડેટા 구현: ../ઉપકરણો/અમલ_કરો_આદેશ.py"""
import importlib as 가져오기
import sys as ઑપરેટિંગ_સિસ્ટમ_મૂલ્ય
from pathlib import Path as પથ
ઑપરેટિંગ_સિસ્ટમ_મૂલ્ય.path.insert(0, str(પથ(__file__).resolve().parents[1] / 'ઉપકરણો'))
if __name__ == '__main__':
    import runpy as એપ્લિકેશન_લૉન્ચર
    એપ્લિકેશન_લૉન્ચર.run_module('અમલ_કરો_આદેશ', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('અમલ_કરો_આદેશ')
    대응 = {'supported': '지원목록', 'parser': '인수해석기', 'qemu': '모의기계', 'run_desktop': 'ચલાવો_ડેસ્કટૉપ', 'main': 'ચલાવો_2', 'host': 'હોસ્ટ', 'status': 'સ્થિતિ_મૂલ્ય_e10195a1', 'NetworkBridge': 'નેટવર્ક_બ્રિજ', 'ROOT': 'પ્રોજેક્ટ_રૂટ', 'bridge': 'બ્રિજ', 'loader': '적재기', 'base': 'વૉલપેપર_મૂલ્ય', 'options': 'વિકલ્પો', 'binary': 'બાઇનરી', 'args': 'દલીલ_અરે', 'command': 'આદેશ'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
