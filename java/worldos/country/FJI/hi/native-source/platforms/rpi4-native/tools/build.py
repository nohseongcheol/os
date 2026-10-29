#!/usr/bin/env python3
"""기존 पथ 호환 प्रवेश_बिदुं. वास्तविक_डेटा 구현: ../उपकरण/बिल्ड_सिस्टम.py"""
import importlib as 가져오기
import sys as ऑपरेटिंग_सिस्टम_मान
from pathlib import Path as पथ
ऑपरेटिंग_सिस्टम_मान.path.insert(0, str(पथ(__file__).resolve().parents[1] / 'उपकरण'))
if __name__ == '__main__':
    import runpy as ऐप_लॉन्चर
    ऐप_लॉन्चर.run_module('बिल्ड_सिस्टम', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('बिल्ड_सिस्टम')
    대응 = {'network': 'नेटवर्क', 'BUILD': 'बिल्ड_पथ', 'ar': 'संग्रह_उपकरण', 'build_examples': '예제만들기', 'posix': '포직스경로', 'font_data': 'फ़ॉन्ट_डेटा', 'flags': 'कॉन्फ़िगरेशन_बैकग्राउंड_इंटेलिजेंट_ट्रांसफ़र_सर्विस', 'a': '첫째값', 'cc': 'सी_कंपाइलर', 'args': 'तर्क_सरणी', 'source_flags': '원본설정', 'ld': '연결편집기', 'method': 'विधि_एन्ट्री', 'main': 'चलाएँ', 'objcopy': 'ऑब्जेक्ट_फ़ाइल_परिर्वतक', 'ROOT': 'प्रोजेक्ट_करें_मूल', 'cxx': '시플플번역기', 'includes': '포함인수', 'compiler': 'कंपाइलर_उपकरण', 'build_users': 'बनाएँ_उपयोगकर्ता_स्थान', 'f': 'फ़ाइल_एन्ट्री', 'extra': '추가영역', 'exports': 'निर्यात_करें_तालिका', 'jobs': '빌드작업', 'run': 'निष्पादित_करें_आदेश', 'path': 'पथ', 'REPO': 'संग्रह_मूल', 'tool': 'उपकरण', 'classes': 'कक्षा_पथ', 'output': '출력결과', 'samples': '예제들', 'symbol': 'प्रतीक_मान', 'source': '원본자료', 'name': 'नाम', 'build_network': 'बनाएँ_नेटवर्क', 'font_info': 'फ़ॉन्ट_जानकारी', 'manifest': 'बंडल_सूची', 'work': '작업경로'}
    for 이전, अद्यतित_आइटम in 대응.items():
        if hasattr(구현, अद्यतित_आइटम): globals()[이전] = getattr(구현, अद्यतित_आइटम)
