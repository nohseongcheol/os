#!/usr/bin/env python3
"""기존 પથ 호환 પ્રવેશ_બિંદુ. વાસ્તવિક_ડેટા 구현: ../ઉપકરણો/બિલ્ડ_ઉપયોગકર્તા_જગ્યા.py"""
import importlib as 가져오기
import sys as ઑપરેટિંગ_સિસ્ટમ_મૂલ્ય
from pathlib import Path as પથ
ઑપરેટિંગ_સિસ્ટમ_મૂલ્ય.path.insert(0, str(પથ(__file__).resolve().parents[1] / 'ઉપકરણો'))
if __name__ == '__main__':
    import runpy as એપ્લિકેશન_લૉન્ચર
    એપ્લિકેશન_લૉન્ચર.run_module('બિલ્ડ_ઉપયોગકર્તા_જગ્યા', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('બિલ્ડ_ઉપયોગકર્તા_જગ્યા')
    대응 = {'mode': 'પદ્ધતિ_મોડ', 'header': 'શીર્ષલેખ_મૂલ્ય', 'i': '순번', 'build_ccompiler': '시언어번역기만들기', 'ar': 'સંગ્રહ_ઉપકરણ', 'posix': '포직스경로', 'payload': 'પેલોડ_ડેટા', 'flags': '설정비트', 'cases': '시험사례', 'cc': '시언어번역기', 'data': 'ડેટા', 'build_java_library': '자바라이브러리만들기', 'ld': '연결편집기', 'repo': '저장소경로', 'build_python': '파이썬만들기', 'inc': '포함경로', 'argument': '전달값', 'text': 'લખાણ', 'headers': 'શીર્ષલેખ_સૂચી', 'cxx': '시플플번역기', 'valid': '유효함', 'build': 'બિલ્ડ', 'build_users': 'બનાવો_ઉપયોગકર્તા_જગ્યા', 'compiler': '번역기', 'uzlib': '압축해제경로', 'extra': '추가영역', 'phoff': 'એપ્લિકેશન_શીર્ષલેખ_ઑફસેટ', 'offset': 'ઑફસેટ_મૂલ્ય', 'text_address': 'આદેશ_સરનામું', 'abi': '호출규약', 'assembly': '어셈블리자료', 'run': 'અમલ_કરો_આદેશ', 'path': 'પથ', 'p': 'ડેટા_સ્થિતિ', 'changed': '바뀐자료', 'n': '개수', 'flag': 'સેટિંગ્સ_મૂલ્ય', 'index': 'લુકઅપ_અનુક્રમણિકા', 'classes': 'વર્ગ_પાથ', 'output': '출력결과', 'loads': '적재구획', 'data_address': 'ડેટા_સરનામું', 'symbol': 'પ્રતીક_મૂલ્ય', 'root': 'રૂટ_સરનામું', 'patches': '수정사항', 'source': '원본자료', 'sizes': '크기목록', 'blobs': '탑재덩이들', 'name': 'નામ', 'value': 'મૂલ્ય', 'fmt': 'સ્વરૂપ_932e03c8', 'work': '작업경로'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
