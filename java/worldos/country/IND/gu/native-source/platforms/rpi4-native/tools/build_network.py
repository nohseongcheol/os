#!/usr/bin/env python3
"""기존 પથ 호환 પ્રવેશ_બિંદુ. વાસ્તવિક_ડેટા 구현: ../ઉપકરણો/બિલ્ડ_નેટવર્ક.py"""
import importlib as 가져오기
import sys as ઑપરેટિંગ_સિસ્ટમ_મૂલ્ય
from pathlib import Path as પથ
ઑપરેટિંગ_સિસ્ટમ_મૂલ્ય.path.insert(0, str(પથ(__file__).resolve().parents[1] / 'ઉપકરણો'))
if __name__ == '__main__':
    import runpy as એપ્લિકેશન_લૉન્ચર
    એપ્લિકેશન_લૉન્ચર.run_module('બિલ્ડ_નેટવર્ક', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('બિલ્ડ_નેટવર્ક')
    대응 = {'obj': 'ગંતવ્ય_ફાઇલ', 'objects': 'ગંતવ્ય_ફાઇલો', 'library': 'લાઇબ્રેરી', 'output': '출력결과', 'port': 'પોર્ટ_નંબર', 'root': 'રૂટ_સરનામું', 'files': 'ફાઇલ_સૂચી', 'source': '원본자료', 'run': 'અમલ_કરો_આદેશ', 'flags': '설정비트', 'path': 'પથ', 'build_network': 'બનાવો_નેટવર્ક_48d29d6d', 'cc': '시언어번역기', 'ar': 'સંગ્રહ_ઉપકરણ'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
