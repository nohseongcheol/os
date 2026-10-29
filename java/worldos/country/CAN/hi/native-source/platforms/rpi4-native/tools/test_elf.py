#!/usr/bin/env python3
"""기존 पथ 호환 प्रवेश_बिदुं. वास्तविक_डेटा 구현: ../उपकरण/실행파일시험.py"""
import importlib as 가져오기
import sys as ऑपरेटिंग_सिस्टम_मान
from pathlib import Path as पथ
ऑपरेटिंग_सिस्टम_मान.path.insert(0, str(पथ(__file__).resolve().parents[1] / 'उपकरण'))
if __name__ == '__main__':
    import runpy as ऐप_लॉन्चर
    ऐप_लॉन्चर.run_module('실행파일시험', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('실행파일시험')
    대응 = {'out': 'परिणाम_डेटा', 'expected': '예상결과', 'phoff': 'ऐप_हेडर_ऑफ़सेट', 'offset': 'ऑफ़सेट_मान', 'invalid': 'अमान्य_डेटा', 'path': 'पथ', 'executable': 'निष्पादन_योग्य_फ़ाइल_छवि', 'rejected': '거부결과', 'linux_example': '리눅스예제', 'original': '원본', 'result': 'परिणाम', 'format_': 'फॉर्मैट_b87fd068', 'main': 'चलाएँ', 'content': 'सामग्री_मान', 'source': '원본자료', 'name': 'नाम', 'reference': 'तुलना_आधार_रेखा', 'ROOT': 'प्रोजेक्ट_करें_मूल', 'value': 'मान', 'report': 'प्रमाणीकरण_रिपोर्ट'}
    for 이전, अद्यतित_आइटम in 대응.items():
        if hasattr(구현, अद्यतित_आइटम): globals()[이전] = getattr(구현, अद्यतित_आइटम)
