#!/usr/bin/env python3
"""기존 पाथ 호환 प्रवेश_पॉयंट. प्रत्यक्ष_डेटा 구현: ../साधनां/코딩시험.py"""
import importlib as TAKE_मोल
import sys as ऑपरेटिंग_प्रणाली_मोल
from pathlib import Path as पाथ
ऑपरेटिंग_प्रणाली_मोल.path.insert(0, str(पाथ(__file__).resolve().parents[1] / 'साधनां'))
if __name__ == '__main__':
    import runpy as एप्लिकेशन_ऍप्लिकेशन_ड्रॉवर
    एप्लिकेशन_ऍप्लिकेशन_ड्रॉवर.run_module('코딩시험', run_name='__main__', alter_sys=True)
else:
    구현 = TAKE_मोल.import_module('코딩시험')
    대응 = {'out': 'मेजप_डेटा', 'expected': '예상결과', 'sdk': '개발꾸러미', 'suffix': '뒷부분', 'arc': '압축묶음', 'main': 'चलोवप', 'elf': '실행파일', 'run': 'पाळो_दिवचो_आदेश', 'name': 'नांव', 'path': 'पाथ', 'p': 'डेटा_स्थिती', 'ROOT': 'प्रॉजॅक्ट_रूट', 'report': 'वैधताय_अहवाल', 'args': 'युक्तीवाद_क्रम'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
