#!/usr/bin/env python3
"""기존 വഴി 호환 എന്_ട്രി_പോയിന്_റ്. വാസ്തവമായ_ഡാറ്റാ 구현: ../ഉപകരണങ്ങൾ/자바가상기계시험.py"""
import importlib as 가져오기
import sys as ഓപ്പറേറ്റിംഗ്_സിസ്റ്റം_മൂല്യം
from pathlib import Path as വഴി
ഓപ്പറേറ്റിംഗ്_സിസ്റ്റം_മൂല്യം.path.insert(0, str(വഴി(__file__).resolve().parents[1] / 'ഉപകരണങ്ങൾ'))
if __name__ == '__main__':
    import runpy as പ്രോഗ്രാം_ആപ്പ്_ഡ്രോയർ
    പ്രോഗ്രാം_ആപ്പ്_ഡ്രോയർ.run_module('자바가상기계시험', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('자바가상기계시험')
    대응 = {'message': '알림문', 's': 'സ്ട്രിംഗ്_ഡാറ്റാ', 'actual': 'വാസ്തവമായ_അളവ്', 'match': '일치', 'payload': 'പേലോഡ്_ഡാറ്റാ', 'cases': 'കേസ്_പരിശോധന', 'fixture': '시험자료', 'main': 'നടപ്പിലാക്കുക', 'ROOT': 'പ്രൊജക്റ്റ്_ചെയ്യുക_വർഗ്ഗമൂലം', 'text': 'പദാവലി', 'valid': 'സാധുതയുളള', 'includes': '포함인수', 'include': '포함항목', 'expected': '예상결과', 'sources': '원문목록', 'tmp': '임시경로', 'done': '완료량', 'classes': 'ക്ലാസ്_പാത', 'output': '출력결과', 'result': 'അളവ്', 'cmd': '명령인수', 'name': 'പേരു്', 'jar': '자바꾸러미', 'report': 'నిర్ధారణ_నివేదిక', 'tests': 'പരിശോധന_ലിസ്റ്റ്'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
