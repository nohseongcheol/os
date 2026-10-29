#!/usr/bin/env python3
"""기존 पथ 호환 प्रवेश_बिदुं. वास्तविक_डेटा 구현: ../उपकरण/예제빌드.py"""
import importlib as 가져오기
import sys as ऑपरेटिंग_सिस्टम_मान
from pathlib import Path as पथ
ऑपरेटिंग_सिस्टम_मान.path.insert(0, str(पथ(__file__).resolve().parents[1] / 'उपकरण'))
if __name__ == '__main__':
    import runpy as ऐप_लॉन्चर
    ऐप_लॉन्चर.run_module('예제빌드', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('예제빌드')
    대응 = {'out': 'परिणाम_डेटा', 'build_examples': '예제만들기', 'files': 'फ़ाइल_सूची', 'java': '자바실행', 'run': 'निष्पादित_करें_आदेश', 'path': 'पथ', 'p': 'डेटा_पद', 'readme': 'ReadMe_फ़ाइल', 'build_java_library': '자바라이브러리만들기', 'code': '명령열', 'index': 'लुकअप_इंडेक्स', 'classes': 'कक्षा_पथ', 'repo': 'संग्रह_पथ', 'root': 'मूल_पता', 'content': 'सामग्री_मान', 'source': '원본자료', 'name': 'नाम', 'target': 'लक्ष्य', 'manifest': 'बंडल_सूची', 'language': 'भाषा'}
    for 이전, अद्यतित_आइटम in 대응.items():
        if hasattr(구현, अद्यतित_आइटम): globals()[이전] = getattr(구현, अद्यतित_आइटम)
