#!/usr/bin/env python3
"""기존 വഴി 호환 എന്_ട്രി_പോയിന്_റ്. വാസ്തവമായ_ഡാറ്റാ 구현: ../ഉപകരണങ്ങൾ/개발꾸러미내보내기.py"""
import importlib as 가져오기
import sys as ഓപ്പറേറ്റിംഗ്_സിസ്റ്റം_മൂല്യം
from pathlib import Path as വഴി
ഓപ്പറേറ്റിംഗ്_സിസ്റ്റം_മൂല്യം.path.insert(0, str(വഴി(__file__).resolve().parents[1] / 'ഉപകരണങ്ങൾ'))
if __name__ == '__main__':
    import runpy as പ്രോഗ്രാം_ആപ്പ്_ഡ്രോയർ
    പ്രോഗ്രാം_ആപ്പ്_ഡ്രോയർ.run_module('개발꾸러미내보내기', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('개발꾸러미내보내기')
    대응 = {'out': 'അളവ്_ഡാറ്റാ', 'obj': 'ഉദ്ദിഷ്ടസ്ഥാന_ഫയല്', 'relative': 'ആപേക്ഷിക_പാത', 'compiler_archive': '번역기꾸러미', 'sdk': '개발꾸러미', 'dist': '배포경로', 'archive': 'ശേഖരം', 'main': 'നടപ്പിലാക്കുക', 'posix': '포직스경로', 'files': 'ഫയല്_ലിസ്റ്റ്', 'source': '원본자료', 'name': 'പേരു്', 'target': 'ലക്_ഷ്യം', 'ROOT': 'പ്രൊജക്റ്റ്_ചെയ്യുക_വർഗ്ഗമൂലം', 'destination': 'ഉദ്ദിഷ്ടസ്ഥാനം_ഡാറ്റാ_ഇമെയിൽ', 'manifest': 'ബണ്ടിൽ_ആവിഷ്കാരം', 'work': '작업경로'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
