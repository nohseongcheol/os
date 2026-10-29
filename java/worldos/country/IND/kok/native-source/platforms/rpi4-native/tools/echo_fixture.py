#!/usr/bin/env python3
"""기존 पाथ 호환 प्रवेश_पॉयंट. प्रत्यक्ष_डेटा 구현: ../साधनां/되돌림시험서버.py"""
import importlib as TAKE_मोल
import sys as ऑपरेटिंग_प्रणाली_मोल
from pathlib import Path as पाथ
ऑपरेटिंग_प्रणाली_मोल.path.insert(0, str(पाथ(__file__).resolve().parents[1] / 'साधनां'))
if __name__ == '__main__':
    import runpy as एप्लिकेशन_ऍप्लिकेशन_ड्रॉवर
    एप्लिकेशन_ऍप्लिकेशन_ड्रॉवर.run_module('되돌림시험서버', run_name='__main__', alter_sys=True)
else:
    구현 = TAKE_मोल.import_module('되돌림시험서버')
    대응 = {'data': 'डेटा', 'e': '보조항목', 'connection': 'कनॅक्शन_e05f319b', 'f': 'फायल_प्रवेश', 'peer': 'पीयर_मोल', 'self': '자신', 'udp': '전문제어', 't': 'टर्मिनल_प्रवेश', 'tcp': 'कनॅक्शन_नियंत्रण', 'EchoFixture': '되돌림시험서버', 'args': 'युक्तीवाद_क्रम', 'chunk': '조각'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
