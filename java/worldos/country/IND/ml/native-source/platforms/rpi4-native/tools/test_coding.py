#!/usr/bin/env python3
"""기존 വഴി 호환 എന്_ട്രി_പോയിന്_റ്. വാസ്തവമായ_ഡാറ്റാ 구현: ../ഉപകരണങ്ങൾ/코딩시험.py"""
import importlib as 가져오기
import sys as ഓപ്പറേറ്റിംഗ്_സിസ്റ്റം_മൂല്യം
from pathlib import Path as വഴി
ഓപ്പറേറ്റിംഗ്_സിസ്റ്റം_മൂല്യം.path.insert(0, str(വഴി(__file__).resolve().parents[1] / 'ഉപകരണങ്ങൾ'))
if __name__ == '__main__':
    import runpy as പ്രോഗ്രാം_ആപ്പ്_ഡ്രോയർ
    പ്രോഗ്രാം_ആപ്പ്_ഡ്രോയർ.run_module('코딩시험', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('코딩시험')
    대응 = {'out': 'അളവ്_ഡാറ്റാ', 'expected': '예상결과', 'sdk': '개발꾸러미', 'suffix': '뒷부분', 'arc': '압축묶음', 'main': 'നടപ്പിലാക്കുക', 'elf': 'നിര്_വ്വഹണക്ഷമമായ_ഫയല്', 'run': 'നടപ്പാക്കുക_കമാന്_ഡ്', 'name': 'പേരു്', 'path': 'വഴി', 'p': 'ഡാറ്റാ_പദവി', 'ROOT': 'പ്രൊജക്റ്റ്_ചെയ്യുക_വർഗ്ഗമൂലം', 'report': 'నిర్ధారణ_నివేదిక', 'args': 'ആര്_ഗ്യുമെന്_റ്_അരേ'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
