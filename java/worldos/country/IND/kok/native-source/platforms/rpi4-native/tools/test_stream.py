#!/usr/bin/env python3
"""기존 पाथ 호환 प्रवेश_पॉयंट. प्रत्यक्ष_डेटा 구현: ../साधनां/흐름시험.py"""
import importlib as TAKE_मोल
import sys as ऑपरेटिंग_प्रणाली_मोल
from pathlib import Path as पाथ
ऑपरेटिंग_प्रणाली_मोल.path.insert(0, str(पाथ(__file__).resolve().parents[1] / 'साधनां'))
if __name__ == '__main__':
    import runpy as एप्लिकेशन_ऍप्लिकेशन_ड्रॉवर
    एप्लिकेशन_ऍप्लिकेशन_ड्रॉवर.run_module('흐름시험', run_name='__main__', alter_sys=True)
else:
    구현 = TAKE_मोल.import_module('흐름시험')
    대응 = {'out': 'मेजप_डेटा', 'main': 'चलोवप', 'ROOT': 'प्रॉजॅक्ट_रूट', 'p': 'डेटा_स्थिती', 'text': 'SMS', 'report': 'वैधताय_अहवाल'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
