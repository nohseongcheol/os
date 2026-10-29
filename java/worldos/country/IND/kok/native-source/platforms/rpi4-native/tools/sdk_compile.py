#!/usr/bin/env python3
"""기존 पाथ 호환 प्रवेश_पॉयंट. प्रत्यक्ष_डेटा 구현: ../साधनां/개발꾸러미번역.py"""
import importlib as TAKE_मोल
import sys as ऑपरेटिंग_प्रणाली_मोल
from pathlib import Path as पाथ
ऑपरेटिंग_प्रणाली_मोल.path.insert(0, str(पाथ(__file__).resolve().parents[1] / 'साधनां'))
if __name__ == '__main__':
    import runpy as एप्लिकेशन_ऍप्लिकेशन_ड्रॉवर
    एप्लिकेशन_ऍप्लिकेशन_ड्रॉवर.run_module('개발꾸러미번역', run_name='__main__', alter_sys=True)
else:
    구현 = TAKE_मोल.import_module('개발꾸러미번역')
    대응 = {'compiler': '번역기', 'obj': 'नियुक्त_स्थानाची_फायल', 'sdk': '개발꾸러미', 'output': '출력결과', 'main': 'चलोवप', 'elf': '실행파일', 'is_c': '시언어여부', 'parser': '인수해석기', 'language': 'भास', 'work': '작업경로', 'args': 'युक्तीवाद_क्रम'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
