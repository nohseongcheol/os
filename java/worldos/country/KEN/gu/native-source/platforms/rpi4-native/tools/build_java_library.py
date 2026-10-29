#!/usr/bin/env python3
"""기존 પથ 호환 પ્રવેશ_બિંદુ. વાસ્તવિક_ડેટા 구현: ../ઉપકરણો/자바라이브러리빌드.py"""
import importlib as 가져오기
import sys as ઑપરેટિંગ_સિસ્ટમ_મૂલ્ય
from pathlib import Path as પથ
ઑપરેટિંગ_સિસ્ટમ_મૂલ્ય.path.insert(0, str(પથ(__file__).resolve().parents[1] / 'ઉપકરણો'))
if __name__ == '__main__':
    import runpy as એપ્લિકેશન_લૉન્ચર
    એપ્લિકેશન_લૉન્ચર.run_module('자바라이브러리빌드', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('자바라이브러리빌드')
    대응 = {'header': 'શીર્ષલેખ_મૂલ્ય', 'sources': '원문목록', 'i': '순번', 'info': 'સિસ્ટમ_માહિતી', 'payload': 'પેલોડ_ડેટા', 'src': '원본주소', 'run': 'અમલ_કરો_આદેશ', 'build_java_library': '자바라이브러리만들기', 'relative': '상대경로', 'classes': 'વર્ગ_પાથ', 'dist': '배포경로', 'archive': 'સંગ્રહ', 'output': '출력결과', 'root': 'રૂટ_સરનામું', 'name': 'નામ', 'jar': '자바꾸러미', 'b': '둘째값', 'entries': '항목들'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
