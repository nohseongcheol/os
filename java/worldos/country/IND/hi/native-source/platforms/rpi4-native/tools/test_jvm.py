#!/usr/bin/env python3
"""기존 पथ 호환 प्रवेश_बिदुं. वास्तविक_डेटा 구현: ../उपकरण/자바가상기계시험.py"""
import importlib as 가져오기
import sys as ऑपरेटिंग_सिस्टम_मान
from pathlib import Path as पथ
ऑपरेटिंग_सिस्टम_मान.path.insert(0, str(पथ(__file__).resolve().parents[1] / 'उपकरण'))
if __name__ == '__main__':
    import runpy as ऐप_लॉन्चर
    ऐप_लॉन्चर.run_module('자바가상기계시험', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('자바가상기계시험')
    대응 = {'message': 'सूचना_पाठ', 's': 'स्ट्रिंग_डेटा', 'actual': 'वास्तविक_परिणाम', 'match': '일치', 'payload': 'पेलोड_डेटा', 'cases': 'परिक्षण_विषय', 'fixture': '시험자료', 'main': 'चलाएँ', 'ROOT': 'प्रोजेक्ट_करें_मूल', 'text': 'पाठ', 'valid': 'वैध', 'includes': '포함인수', 'include': '포함항목', 'expected': '예상결과', 'sources': '원문목록', 'tmp': '임시경로', 'done': 'पूर्ण_राशि', 'classes': 'कक्षा_पथ', 'output': '출력결과', 'result': 'परिणाम', 'cmd': '명령인수', 'name': 'नाम', 'jar': '자바꾸러미', 'report': 'प्रमाणीकरण_रिपोर्ट', 'tests': 'परिक्षण_सूची'}
    for 이전, अद्यतित_आइटम in 대응.items():
        if hasattr(구현, अद्यतित_आइटम): globals()[이전] = getattr(구현, अद्यतित_आइटम)
