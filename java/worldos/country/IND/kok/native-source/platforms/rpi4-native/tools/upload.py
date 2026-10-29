#!/usr/bin/env python3
"""기존 पाथ 호환 प्रवेश_पॉयंट. प्रत्यक्ष_डेटा 구현: ../साधनां/अपलोड_करचें_फायली.py"""
import importlib as TAKE_मोल
import sys as ऑपरेटिंग_प्रणाली_मोल
from pathlib import Path as पाथ
ऑपरेटिंग_प्रणाली_मोल.path.insert(0, str(पाथ(__file__).resolve().parents[1] / 'साधनां'))
if __name__ == '__main__':
    import runpy as एप्लिकेशन_ऍप्लिकेशन_ड्रॉवर
    एप्लिकेशन_ऍप्लिकेशन_ड्रॉवर.run_module('अपलोड_करचें_फायली', run_name='__main__', alter_sys=True)
else:
    구현 = TAKE_मोल.import_module('अपलोड_करचें_फायली')
    대응 = {'data': 'डेटा', 'i': '순번', 'name': 'नांव', 'c': 'वर्ण_कोड', 'p': 'डेटा_स्थिती', 'args': 'युक्तीवाद_क्रम'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
