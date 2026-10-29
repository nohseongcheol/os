#!/usr/bin/env python3
"""기존 വഴി 호환 എന്_ട്രി_പോയിന്_റ്. വാസ്തവമായ_ഡാറ്റാ 구현: ../ഉപകരണങ്ങൾ/되돌림시험서버.py"""
import importlib as 가져오기
import sys as ഓപ്പറേറ്റിംഗ്_സിസ്റ്റം_മൂല്യം
from pathlib import Path as വഴി
ഓപ്പറേറ്റിംഗ്_സിസ്റ്റം_മൂല്യം.path.insert(0, str(വഴി(__file__).resolve().parents[1] / 'ഉപകരണങ്ങൾ'))
if __name__ == '__main__':
    import runpy as പ്രോഗ്രാം_ആപ്പ്_ഡ്രോയർ
    പ്രോഗ്രാം_ആപ്പ്_ഡ്രോയർ.run_module('되돌림시험서버', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('되돌림시험서버')
    대응 = {'data': 'ഡാറ്റാ', 'e': '보조항목', 'connection': 'കണക്ഷൻ_e05f319b', 'f': 'ഫയല്_എന്_ട്രി', 'peer': 'പീര്_മൂല്യം', 'self': '자신', 'udp': '전문제어', 't': 'ടെർമിനൽ_എന്_ട്രി', 'tcp': 'കണക്ഷൻ_നിയന്ത്രണം', 'EchoFixture': '되돌림시험서버', 'args': 'ആര്_ഗ്യുമെന്_റ്_അരേ', 'chunk': '조각'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
