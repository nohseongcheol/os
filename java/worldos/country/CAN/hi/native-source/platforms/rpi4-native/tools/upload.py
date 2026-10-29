#!/usr/bin/env python3
"""기존 पथ 호환 प्रवेश_बिदुं. वास्तविक_डेटा 구현: ../उपकरण/अपलोड_फ़ाइलें.py"""
import importlib as 가져오기
import sys as ऑपरेटिंग_सिस्टम_मान
from pathlib import Path as पथ
ऑपरेटिंग_सिस्टम_मान.path.insert(0, str(पथ(__file__).resolve().parents[1] / 'उपकरण'))
if __name__ == '__main__':
    import runpy as ऐप_लॉन्चर
    ऐप_लॉन्चर.run_module('अपलोड_फ़ाइलें', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('अपलोड_फ़ाइलें')
    대응 = {'data': 'आँकड़े', 'i': '순번', 'name': 'नाम', 'c': 'वर्ण_कोड', 'p': 'डेटा_पद', 'args': 'तर्क_सरणी'}
    for 이전, अद्यतित_आइटम in 대응.items():
        if hasattr(구현, अद्यतित_आइटम): globals()[이전] = getattr(구현, अद्यतित_आइटम)
