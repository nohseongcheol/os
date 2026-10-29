#!/usr/bin/env python3
"""기존 पाथ 호환 प्रवेश_पॉयंट. प्रत्यक्ष_डेटा 구현: ../साधनां/자바가상기계시험.py"""
import importlib as TAKE_मोल
import sys as ऑपरेटिंग_प्रणाली_मोल
from pathlib import Path as पाथ
ऑपरेटिंग_प्रणाली_मोल.path.insert(0, str(पाथ(__file__).resolve().parents[1] / 'साधनां'))
if __name__ == '__main__':
    import runpy as एप्लिकेशन_ऍप्लिकेशन_ड्रॉवर
    एप्लिकेशन_ऍप्लिकेशन_ड्रॉवर.run_module('자바가상기계시험', run_name='__main__', alter_sys=True)
else:
    구현 = TAKE_मोल.import_module('자바가상기계시험')
    대응 = {'message': '알림문', 's': 'स्ट्रिंग_डेटा', 'actual': 'प्रत्यक्ष_मेजप', 'match': '일치', 'payload': 'पेलोड_डेटा', 'cases': '시험사례', 'fixture': '시험자료', 'main': 'चलोवप', 'ROOT': 'प्रॉजॅक्ट_रूट', 'text': 'SMS', 'valid': '유효함', 'includes': '포함인수', 'include': '포함항목', 'expected': '예상결과', 'sources': '원문목록', 'tmp': '임시경로', 'done': '완료량', 'classes': 'वर्ग_पाथ', 'output': '출력결과', 'result': 'मेजप', 'cmd': '명령인수', 'name': 'नांव', 'jar': '자바꾸러미', 'report': 'वैधताय_अहवाल', 'tests': '시험목록'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
