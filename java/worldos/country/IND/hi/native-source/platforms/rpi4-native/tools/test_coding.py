#!/usr/bin/env python3
"""기존 पथ 호환 प्रवेश_बिदुं. वास्तविक_डेटा 구현: ../उपकरण/코딩시험.py"""
import importlib as 가져오기
import sys as ऑपरेटिंग_सिस्टम_मान
from pathlib import Path as पथ
ऑपरेटिंग_सिस्टम_मान.path.insert(0, str(पथ(__file__).resolve().parents[1] / 'उपकरण'))
if __name__ == '__main__':
    import runpy as ऐप_लॉन्चर
    ऐप_लॉन्चर.run_module('코딩시험', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('코딩시험')
    대응 = {'out': 'परिणाम_डेटा', 'expected': '예상결과', 'sdk': 'डेवलपमेंट_किट', 'suffix': '뒷부분', 'arc': '압축묶음', 'main': 'चलाएँ', 'elf': 'निष्पादन_योग्य_फ़ाइल', 'run': 'निष्पादित_करें_आदेश', 'name': 'नाम', 'path': 'पथ', 'p': 'डेटा_पद', 'ROOT': 'प्रोजेक्ट_करें_मूल', 'report': 'प्रमाणीकरण_रिपोर्ट', 'args': 'तर्क_सरणी'}
    for 이전, अद्यतित_आइटम in 대응.items():
        if hasattr(구현, अद्यतित_आइटम): globals()[이전] = getattr(구현, अद्यतित_आइटम)
