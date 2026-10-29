#!/usr/bin/env python3
"""기존 પથ 호환 પ્રવેશ_બિંદુ. વાસ્તવિક_ડેટા 구현: ../ઉપકરણો/예제빌드.py"""
import importlib as 가져오기
import sys as ઑપરેટિંગ_સિસ્ટમ_મૂલ્ય
from pathlib import Path as પથ
ઑપરેટિંગ_સિસ્ટમ_મૂલ્ય.path.insert(0, str(પથ(__file__).resolve().parents[1] / 'ઉપકરણો'))
if __name__ == '__main__':
    import runpy as એપ્લિકેશન_લૉન્ચર
    એપ્લિકેશન_લૉન્ચર.run_module('예제빌드', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('예제빌드')
    대응 = {'out': 'પરિમાણ_ડેટા', 'build_examples': '예제만들기', 'files': 'ફાઇલ_સૂચી', 'java': '자바실행', 'run': 'અમલ_કરો_આદેશ', 'path': 'પથ', 'p': 'ડેટા_સ્થિતિ', 'readme': 'રીડમી', 'build_java_library': '자바라이브러리만들기', 'code': '명령열', 'index': 'લુકઅપ_અનુક્રમણિકા', 'classes': 'વર્ગ_પાથ', 'repo': '저장소경로', 'root': 'રૂટ_સરનામું', 'content': 'સામગ્રી_મૂલ્ય', 'source': '원본자료', 'name': 'નામ', 'target': 'લક્ષ્ય', 'manifest': '꾸러미명세', 'language': 'ભાષા'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
