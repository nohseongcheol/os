#!/usr/bin/env python3
"""기존 पथ 호환 प्रवेश_बिदुं. वास्तविक_डेटा 구현: ../उपकरण/자바라이브러리빌드.py"""
import importlib as 가져오기
import sys as ऑपरेटिंग_सिस्टम_मान
from pathlib import Path as पथ
ऑपरेटिंग_सिस्टम_मान.path.insert(0, str(पथ(__file__).resolve().parents[1] / 'उपकरण'))
if __name__ == '__main__':
    import runpy as ऐप_लॉन्चर
    ऐप_लॉन्चर.run_module('자바라이브러리빌드', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('자바라이브러리빌드')
    대응 = {'header': 'हेडर_मान', 'sources': '원문목록', 'i': '순번', 'info': 'सिस्टम_जानकारी', 'payload': 'पेलोड_डेटा', 'src': '원본주소', 'run': 'निष्पादित_करें_आदेश', 'build_java_library': '자바라이브러리만들기', 'relative': 'संबंधित_पथ', 'classes': 'कक्षा_पथ', 'dist': '배포경로', 'archive': 'संग्रह', 'output': '출력결과', 'root': 'मूल_पता', 'name': 'नाम', 'jar': '자바꾸러미', 'b': '둘째값', 'entries': '항목들'}
    for 이전, अद्यतित_आइटम in 대응.items():
        if hasattr(구현, अद्यतित_आइटम): globals()[이전] = getattr(구현, अद्यतित_आइटम)
