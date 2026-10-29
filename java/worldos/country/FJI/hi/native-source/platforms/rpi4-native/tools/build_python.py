#!/usr/bin/env python3
"""기존 पथ 호환 प्रवेश_बिदुं. वास्तविक_डेटा 구현: ../उपकरण/파이썬빌드.py"""
import importlib as 가져오기
import sys as ऑपरेटिंग_सिस्टम_मान
from pathlib import Path as पथ
ऑपरेटिंग_सिस्टम_मान.path.insert(0, str(पथ(__file__).resolve().parents[1] / 'उपकरण'))
if __name__ == '__main__':
    import runpy as ऐप_लॉन्चर
    ऐप_लॉन्चर.run_module('파이썬빌드', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('파이썬빌드')
    대응 = {'ld': '연결편집기', 'archive': 'संग्रह', 'SHA256': 'प्रमाणीकरण_हैश', 'build_python': '파이썬만들기', 'root': 'मूल_पता', 'source': '원본자료', 'name': 'नाम', 'path': 'पथ', 'VERSION': 'अंक_मान_237a4c94', 'cc': 'सी_कंपाइलर', 'tar': '타르꾸러미', 'newlib': '뉴리브포함경로', 'member': 'सदस्य'}
    for 이전, अद्यतित_आइटम in 대응.items():
        if hasattr(구현, अद्यतित_आइटम): globals()[이전] = getattr(구현, अद्यतित_आइटम)
