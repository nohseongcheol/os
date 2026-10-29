#!/usr/bin/env python3
"""기존 પથ 호환 પ્રવેશ_બિંદુ. વાસ્તવિક_ડેટા 구현: ../ઉપકરણો/અમલ_કરો_ફાઇલ.py"""
import importlib as 가져오기
import sys as ઑપરેટિંગ_સિસ્ટમ_મૂલ્ય
from pathlib import Path as પથ
ઑપરેટિંગ_સિસ્ટમ_મૂલ્ય.path.insert(0, str(પથ(__file__).resolve().parents[1] / 'ઉપકરણો'))
if __name__ == '__main__':
    import runpy as એપ્લિકેશન_લૉન્ચર
    એપ્લિકેશન_લૉન્ચર.run_module('અમલ_કરો_ફાઇલ', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('અમલ_કરો_ફાઇલ')
    대응 = {'timeout': '시간제한', 's': 'સ્ટ્રિંગ_ડેટા', 'i': '순번', 'match': '일치', 'files': 'ફાઇલ_સૂચી', 'program': 'એપ્લિકેશન', 'executable': '실행가능파일', 'args': 'દલીલ_અરે', 'chunk': '조각', 'data': 'ડેટા', 'proc': 'પ્રક્રિયા', 'send': 'મોકલો', 'main': 'ચલાવો_2', 'marker': '확인표시', 'command': 'આદેશ', 'include': '포함항목', 'dumped': '갈무리자료', 'run': 'અમલ_કરો_આદેશ', 'p': 'ડેટા_સ્થિતિ', 'parser': '인수해석기', 'options': 'વિકલ્પો', 'kind': 'શ્રેણી_મૂલ્ય', 'selector': 'પસંદકર્તા', 'upload_data': 'અપલોડ_કરો_ડેટા', 'end': 'અંત_કરો_ઑફસેટ', 'n': '개수', 'd': 'ગંતવ્ય_ડેટા', 'key': '누름값', 'output': '출력결과', 'line': 'લાઇન', 'name': 'નામ', 'upload_name': 'અપલોડ_કરો_નામ', 'receive': '수신하기'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
