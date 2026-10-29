#!/usr/bin/env python3
"""기존 पथ 호환 प्रवेश_बिदुं. वास्तविक_डेटा 구현: ../उपकरण/निष्पादित_करें_आदेश.py"""
import importlib as 가져오기
import sys as ऑपरेटिंग_सिस्टम_मान
from pathlib import Path as पथ
ऑपरेटिंग_सिस्टम_मान.path.insert(0, str(पथ(__file__).resolve().parents[1] / 'उपकरण'))
if __name__ == '__main__':
    import runpy as ऐप_लॉन्चर
    ऐप_लॉन्चर.run_module('निष्पादित_करें_आदेश', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('निष्पादित_करें_आदेश')
    대응 = {'supported': '지원목록', 'parser': 'पार्सर', 'qemu': '모의기계', 'run_desktop': 'चलाएँ_डेस्कटॉप', 'main': 'चलाएँ', 'host': 'आयोजक', 'status': 'अवस्था_मान', 'NetworkBridge': 'ब्रिज_3de4fe3a', 'ROOT': 'प्रोजेक्ट_करें_मूल', 'bridge': 'ब्रिज', 'loader': 'लोडर', 'base': 'वॉलपेपर_मान', 'options': 'विकल्प', 'binary': 'बाइनरी', 'args': 'तर्क_सरणी', 'command': 'आदेश'}
    for 이전, अद्यतित_आइटम in 대응.items():
        if hasattr(구현, अद्यतित_आइटम): globals()[이전] = getattr(구현, अद्यतित_आइटम)
