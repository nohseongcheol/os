#!/usr/bin/env python3
"""기존 પથ 호환 પ્રવેશ_બિંદુ. વાસ્તવિક_ડેટા 구현: ../ઉપકરણો/시언어번역기빌드.py"""
import importlib as 가져오기
import sys as ઑપરેટિંગ_સિસ્ટમ_મૂલ્ય
from pathlib import Path as પથ
ઑપરેટિંગ_સિસ્ટમ_મૂલ્ય.path.insert(0, str(પથ(__file__).resolve().parents[1] / 'ઉપકરણો'))
if __name__ == '__main__':
    import runpy as એપ્લિકેશન_લૉન્ચર
    એપ્લિકેશન_લૉન્ચર.run_module('시언어번역기빌드', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('시언어번역기빌드')
    대응 = {'out': 'પરિમાણ_ડેટા', 'builtins': '내장연산', 'header': 'શીર્ષલેખ_મૂલ્ય', 'sdk': '개발꾸러미', 'build_ccompiler': '시언어번역기만들기', 'i': '순번', 'elf': '실행파일', 'run': 'અમલ_કરો_આદેશ', 'flags': '설정비트', 'path': 'પથ', 'p': 'ડેટા_સ્થિતિ', 'cc': '시언어번역기', 'obj': 'ગંતવ્ય_ફાઇલ', 'flag': 'સેટિંગ્સ_મૂલ્ય', 'ld': '연결편집기', 'objects': 'ગંતવ્ય_ફાઇલો', 'repo': '저장소경로', 'v': '임시값', 'upstream': '외부원문', 'root': 'રૂટ_સરનામું', 'assets': '탑재자료', 'source': '원본자료', 'name': 'નામ', 'includes': '포함인수'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
