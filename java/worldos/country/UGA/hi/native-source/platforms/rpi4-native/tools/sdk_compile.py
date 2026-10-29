#!/usr/bin/env python3
"""기존 पथ 호환 प्रवेश_बिदुं. वास्तविक_डेटा 구현: ../उपकरण/सॉफ़्टवेयर_डेवलपमेंट_किट_कंपाइल.py"""
import importlib as 가져오기
import sys as ऑपरेटिंग_सिस्टम_मान
from pathlib import Path as पथ
ऑपरेटिंग_सिस्टम_मान.path.insert(0, str(पथ(__file__).resolve().parents[1] / 'उपकरण'))
if __name__ == '__main__':
    import runpy as ऐप_लॉन्चर
    ऐप_लॉन्चर.run_module('सॉफ़्टवेयर_डेवलपमेंट_किट_कंपाइल', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('सॉफ़्टवेयर_डेवलपमेंट_किट_कंपाइल')
    대응 = {'compiler': 'कंपाइलर_उपकरण', 'obj': 'गंतव्य_फ़ाइल', 'sdk': 'डेवलपमेंट_किट', 'output': '출력결과', 'main': 'चलाएँ', 'elf': 'निष्पादन_योग्य_फ़ाइल', 'is_c': 'सूचना_प्रौद्योगिकी_सी_भाषा', 'parser': 'पार्सर', 'language': 'भाषा', 'work': '작업경로', 'args': 'तर्क_सरणी'}
    for 이전, अद्यतित_आइटम in 대응.items():
        if hasattr(구현, अद्यतित_आइटम): globals()[이전] = getattr(구현, अद्यतित_आइटम)
