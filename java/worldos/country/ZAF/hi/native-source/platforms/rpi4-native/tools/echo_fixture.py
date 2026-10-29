#!/usr/bin/env python3
"""기존 पथ 호환 प्रवेश_बिदुं. वास्तविक_डेटा 구현: ../उपकरण/되돌림시험서버.py"""
import importlib as 가져오기
import sys as ऑपरेटिंग_सिस्टम_मान
from pathlib import Path as पथ
ऑपरेटिंग_सिस्टम_मान.path.insert(0, str(पथ(__file__).resolve().parents[1] / 'उपकरण'))
if __name__ == '__main__':
    import runpy as ऐप_लॉन्चर
    ऐप_लॉन्चर.run_module('되돌림시험서버', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('되돌림시험서버')
    대응 = {'data': 'आँकड़े', 'e': '보조항목', 'connection': 'कनेक्शन_e05f319b', 'f': 'फ़ाइल_एन्ट्री', 'peer': 'पीअर_मान', 'self': '자신', 'udp': '전문제어', 't': 'टर्मिनल_एन्ट्री', 'tcp': 'कनेक्शन_नियंत्रण', 'EchoFixture': '되돌림시험서버', 'args': 'तर्क_सरणी', 'chunk': '조각'}
    for 이전, अद्यतित_आइटम in 대응.items():
        if hasattr(구현, अद्यतित_आइटम): globals()[이전] = getattr(구현, अद्यतित_आइटम)
