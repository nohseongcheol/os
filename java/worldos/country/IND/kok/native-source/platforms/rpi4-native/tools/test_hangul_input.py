#!/usr/bin/env python3
"""기존 पाथ 호환 प्रवेश_पॉयंट. प्रत्यक्ष_डेटा 구현: ../साधनां/한글입력시험.py"""
import importlib as TAKE_मोल
import sys as ऑपरेटिंग_प्रणाली_मोल
from pathlib import Path as पाथ
ऑपरेटिंग_प्रणाली_मोल.path.insert(0, str(पाथ(__file__).resolve().parents[1] / 'साधनां'))
if __name__ == '__main__':
    import runpy as एप्लिकेशन_ऍप्लिकेशन_ड्रॉवर
    एप्लिकेशन_ऍप्लिकेशन_ड्रॉवर.run_module('한글입력시험', run_name='__main__', alter_sys=True)
else:
    구현 = TAKE_मोल.import_module('한글입력시험')
    대응 = {'expected': '예상결과', 'Keyboard': 'किबोर्ड', 'press': '글쇠누르기', 'self': '자신', 'test_modes_repeat_and_commit': 'test_전환반복확정', 'keys': '누름열', 'test_paste_and_unicode': 'test_붙이기유니코드', 'data': 'डेटा', 'key': '누름값', 'send': 'धाडचें', 'test_words': 'test_낱말', 'InputTests': '한글입력시험', 'test_backspace': 'test_앞글자지우기', 'symbol': 'चिन्न_मोल', 'char': 'वर्ण_डेटा', 'type': 'TYPE_वर्ग'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
