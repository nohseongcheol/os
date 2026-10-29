#!/usr/bin/env python3
"""기존 വഴി 호환 എന്_ട്രി_പോയിന്_റ്. വാസ്തവമായ_ഡാറ്റാ 구현: ../ഉപകരണങ്ങൾ/자바라이브러리빌드.py"""
import importlib as 가져오기
import sys as ഓപ്പറേറ്റിംഗ്_സിസ്റ്റം_മൂല്യം
from pathlib import Path as വഴി
ഓപ്പറേറ്റിംഗ്_സിസ്റ്റം_മൂല്യം.path.insert(0, str(വഴി(__file__).resolve().parents[1] / 'ഉപകരണങ്ങൾ'))
if __name__ == '__main__':
    import runpy as പ്രോഗ്രാം_ആപ്പ്_ഡ്രോയർ
    പ്രോഗ്രാം_ആപ്പ്_ഡ്രോയർ.run_module('자바라이브러리빌드', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('자바라이브러리빌드')
    대응 = {'header': 'ശീർഷകം_മൂല്യം', 'sources': '원문목록', 'i': '순번', 'info': 'സിസ്റ്റം_വിവരങ്ങള്', 'payload': 'പേലോഡ്_ഡാറ്റാ', 'src': '원본주소', 'run': 'നടപ്പാക്കുക_കമാന്_ഡ്', 'build_java_library': '자바라이브러리만들기', 'relative': 'ആപേക്ഷിക_പാത', 'classes': 'ക്ലാസ്_പാത', 'dist': '배포경로', 'archive': 'ശേഖരം', 'output': '출력결과', 'root': 'വർഗ്ഗമൂലം_ഇമെയിൽ', 'name': 'പേരു്', 'jar': '자바꾸러미', 'b': '둘째값', 'entries': '항목들'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
