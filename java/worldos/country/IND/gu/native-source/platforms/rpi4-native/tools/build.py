#!/usr/bin/env python3
"""기존 પથ 호환 પ્રવેશ_બિંદુ. વાસ્તવિક_ડેટા 구현: ../ઉપકરણો/બિલ્ડ_સિસ્ટમ.py"""
import importlib as 가져오기
import sys as ઑપરેટિંગ_સિસ્ટમ_મૂલ્ય
from pathlib import Path as પથ
ઑપરેટિંગ_સિસ્ટમ_મૂલ્ય.path.insert(0, str(પથ(__file__).resolve().parents[1] / 'ઉપકરણો'))
if __name__ == '__main__':
    import runpy as એપ્લિકેશન_લૉન્ચર
    એપ્લિકેશન_લૉન્ચર.run_module('બિલ્ડ_સિસ્ટમ', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('બિલ્ડ_સિસ્ટમ')
    대응 = {'network': 'નેટવર્ક', 'BUILD': 'બિલ્ડ_પાથ', 'ar': 'સંગ્રહ_ઉપકરણ', 'build_examples': '예제만들기', 'posix': '포직스경로', 'font_data': 'ફૉન્ટ_ડેટા', 'flags': '설정비트', 'a': '첫째값', 'cc': '시언어번역기', 'args': 'દલીલ_અરે', 'source_flags': '원본설정', 'ld': '연결편집기', 'method': 'પદ્ધતિ_પ્રવેશ', 'main': 'ચલાવો_2', 'objcopy': 'ઑબ્જેક્ટ_ફાઇલ_કન્વર્ટર', 'ROOT': 'પ્રોજેક્ટ_રૂટ', 'cxx': '시플플번역기', 'includes': '포함인수', 'compiler': '번역기', 'build_users': 'બનાવો_ઉપયોગકર્તા_જગ્યા', 'f': 'ફાઇલ_પ્રવેશ', 'extra': '추가영역', 'exports': 'નિકાસ_કરો_કોષ્ટક', 'jobs': '빌드작업', 'run': 'અમલ_કરો_આદેશ', 'path': 'પથ', 'REPO': '저장소', 'tool': 'ઉપકરણો', 'classes': 'વર્ગ_પાથ', 'output': '출력결과', 'samples': '예제들', 'symbol': 'પ્રતીક_મૂલ્ય', 'source': '원본자료', 'name': 'નામ', 'build_network': 'બનાવો_નેટવર્ક_48d29d6d', 'font_info': 'ફૉન્ટ_માહિતી', 'manifest': '꾸러미명세', 'work': '작업경로'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
