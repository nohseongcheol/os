#!/usr/bin/env python3
"""기존 വഴി 호환 എന്_ട്രി_പോയിന്_റ്. വാസ്തവമായ_ഡാറ്റാ 구현: ../ഉപകരണങ്ങൾ/예제빌드.py"""
import importlib as 가져오기
import sys as ഓപ്പറേറ്റിംഗ്_സിസ്റ്റം_മൂല്യം
from pathlib import Path as വഴി
ഓപ്പറേറ്റിംഗ്_സിസ്റ്റം_മൂല്യം.path.insert(0, str(വഴി(__file__).resolve().parents[1] / 'ഉപകരണങ്ങൾ'))
if __name__ == '__main__':
    import runpy as പ്രോഗ്രാം_ആപ്പ്_ഡ്രോയർ
    പ്രോഗ്രാം_ആപ്പ്_ഡ്രോയർ.run_module('예제빌드', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('예제빌드')
    대응 = {'out': 'അളവ്_ഡാറ്റാ', 'build_examples': '예제만들기', 'files': 'ഫയല്_ലിസ്റ്റ്', 'java': '자바실행', 'run': 'നടപ്പാക്കുക_കമാന്_ഡ്', 'path': 'വഴി', 'p': 'ഡാറ്റാ_പദവി', 'readme': 'readme_ഫയല്', 'build_java_library': '자바라이브러리만들기', 'code': '명령열', 'index': 'തിരഞ്ഞു_നോക്കൽ_സൂചിക', 'classes': 'ക്ലാസ്_പാത', 'repo': 'കലവറ_പാത', 'root': 'വർഗ്ഗമൂലം_ഇമെയിൽ', 'content': 'ഉള്ളടക്കം_മൂല്യം', 'source': '원본자료', 'name': 'പേരു്', 'target': 'ലക്_ഷ്യം', 'manifest': 'ബണ്ടിൽ_ആവിഷ്കാരം', 'language': 'భాష'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
