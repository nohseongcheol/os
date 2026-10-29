#!/usr/bin/env python3
"""기존 पथ 호환 प्रवेश_बिदुं. वास्तविक_डेटा 구현: ../उपकरण/बिल्ड_नेटवर्क.py"""
import importlib as 가져오기
import sys as ऑपरेटिंग_सिस्टम_मान
from pathlib import Path as पथ
ऑपरेटिंग_सिस्टम_मान.path.insert(0, str(पथ(__file__).resolve().parents[1] / 'उपकरण'))
if __name__ == '__main__':
    import runpy as ऐप_लॉन्चर
    ऐप_लॉन्चर.run_module('बिल्ड_नेटवर्क', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('बिल्ड_नेटवर्क')
    대응 = {'obj': 'गंतव्य_फ़ाइल', 'objects': 'गंतव्य_फ़ाइलें', 'library': 'लाइब्रेरी', 'output': '출력결과', 'port': 'पोर्ट_संख्या', 'root': 'मूल_पता', 'files': 'फ़ाइल_सूची', 'source': '원본자료', 'run': 'निष्पादित_करें_आदेश', 'flags': 'कॉन्फ़िगरेशन_बैकग्राउंड_इंटेलिजेंट_ट्रांसफ़र_सर्विस', 'path': 'पथ', 'build_network': 'बनाएँ_नेटवर्क', 'cc': 'सी_कंपाइलर', 'ar': 'संग्रह_उपकरण'}
    for 이전, अद्यतित_आइटम in 대응.items():
        if hasattr(구현, अद्यतित_आइटम): globals()[이전] = getattr(구현, अद्यतित_आइटम)
