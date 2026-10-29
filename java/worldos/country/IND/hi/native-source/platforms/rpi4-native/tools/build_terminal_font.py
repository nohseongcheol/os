#!/usr/bin/env python3
"""기존 पथ 호환 प्रवेश_बिदुं. वास्तविक_डेटा 구현: ../उपकरण/बिल्ड_टर्मिनल_फ़ॉन्ट.py"""
import importlib as 가져오기
import sys as ऑपरेटिंग_सिस्टम_मान
from pathlib import Path as पथ
ऑपरेटिंग_सिस्टम_मान.path.insert(0, str(पथ(__file__).resolve().parents[1] / 'उपकरण'))
if __name__ == '__main__':
    import runpy as ऐप_लॉन्चर
    ऐप_लॉन्चर.run_module('बिल्ड_टर्मिनल_फ़ॉन्ट', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('बिल्ड_टर्मिनल_फ़ॉन्ट')
    대응 = {'data': 'आँकड़े', 'img': 'ड्रॉइंग_मान', 'bits': 'बैकग्राउंड_इंटेलिजेंट_ट्रांसफ़र_सर्विस_सूची', 'x': 'x_निर्देशांक', 'draw': '화면그리기', 'licences': '이용허락목록', 'paths': 'पथ_सूची', 'y': '세로좌표', 'main': 'चलाएँ', 'src': '원본주소', 'fonts': 'फ़ॉन्ट_सूची', 'ROOT': 'प्रोजेक्ट_करें_मूल', 'p': 'डेटा_पद', 'cp': 'वर्ण_एन्_कोडिंग', 'target': 'लक्ष्य'}
    for 이전, अद्यतित_आइटम in 대응.items():
        if hasattr(구현, अद्यतित_आइटम): globals()[이전] = getattr(구현, अद्यतित_आइटम)
