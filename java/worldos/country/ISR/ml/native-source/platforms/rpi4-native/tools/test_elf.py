#!/usr/bin/env python3
"""기존 വഴി 호환 എന്_ട്രി_പോയിന്_റ്. വാസ്തവമായ_ഡാറ്റാ 구현: ../ഉപകരണങ്ങൾ/실행파일시험.py"""
import importlib as 가져오기
import sys as ഓപ്പറേറ്റിംഗ്_സിസ്റ്റം_മൂല്യം
from pathlib import Path as വഴി
ഓപ്പറേറ്റിംഗ്_സിസ്റ്റം_മൂല്യം.path.insert(0, str(വഴി(__file__).resolve().parents[1] / 'ഉപകരണങ്ങൾ'))
if __name__ == '__main__':
    import runpy as പ്രോഗ്രാം_ആപ്പ്_ഡ്രോയർ
    പ്രോഗ്രാം_ആപ്പ്_ഡ്രോയർ.run_module('실행파일시험', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('실행파일시험')
    대응 = {'out': 'അളവ്_ഡാറ്റാ', 'expected': '예상결과', 'phoff': 'പ്രോഗ്രാം_ശീർഷകം_ഓഫ്_സെറ്റ്', 'offset': 'ഓഫ്_സെറ്റ്_മൂല്യം', 'invalid': 'അസാധുവായ_ഡാറ്റാ', 'path': 'വഴി', 'executable': 'നിര്_വ്വഹണക്ഷമമായ_ഫയല്_ഇമേജ്', 'rejected': '거부결과', 'linux_example': '리눅스예제', 'original': '원본', 'result': 'അളവ്', 'format_': 'ఫార్మాట్_b87fd068', 'main': 'നടപ്പിലാക്കുക', 'content': 'ഉള്ളടക്കം_മൂല്യം', 'source': '원본자료', 'name': 'പേരു്', 'reference': 'താരതമ്യം_ఆధారరేఖ', 'ROOT': 'പ്രൊജക്റ്റ്_ചെയ്യുക_വർഗ്ഗമൂലം', 'value': 'മൂല്യം', 'report': 'నిర్ధారణ_నివేదిక'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
