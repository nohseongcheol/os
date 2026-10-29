#!/usr/bin/env python3
"""기존 पथ 호환 प्रवेश_बिदुं. वास्तविक_डेटा 구현: ../उपकरण/निर्यात_करें_सॉफ़्टवेयर_डेवलपमेंट_किट.py"""
import importlib as 가져오기
import sys as ऑपरेटिंग_सिस्टम_मान
from pathlib import Path as पथ
ऑपरेटिंग_सिस्टम_मान.path.insert(0, str(पथ(__file__).resolve().parents[1] / 'उपकरण'))
if __name__ == '__main__':
    import runpy as ऐप_लॉन्चर
    ऐप_लॉन्चर.run_module('निर्यात_करें_सॉफ़्टवेयर_डेवलपमेंट_किट', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('निर्यात_करें_सॉफ़्टवेयर_डेवलपमेंट_किट')
    대응 = {'out': 'परिणाम_डेटा', 'obj': 'गंतव्य_फ़ाइल', 'relative': 'संबंधित_पथ', 'compiler_archive': 'कंपाइलर_संग्रह', 'sdk': 'डेवलपमेंट_किट', 'dist': '배포경로', 'archive': 'संग्रह', 'main': 'चलाएँ', 'posix': '포직스경로', 'files': 'फ़ाइल_सूची', 'source': '원본자료', 'name': 'नाम', 'target': 'लक्ष्य', 'ROOT': 'प्रोजेक्ट_करें_मूल', 'destination': 'गंतव्य_डेटा_पता', 'manifest': 'बंडल_सूची', 'work': '작업경로'}
    for 이전, अद्यतित_आइटम in 대응.items():
        if hasattr(구현, अद्यतित_आइटम): globals()[이전] = getattr(구현, अद्यतित_आइटम)
