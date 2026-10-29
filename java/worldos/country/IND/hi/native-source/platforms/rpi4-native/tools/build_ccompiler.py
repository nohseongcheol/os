#!/usr/bin/env python3
"""기존 पथ 호환 प्रवेश_बिदुं. वास्तविक_डेटा 구현: ../उपकरण/बिल्ड_सी_कंपाइलर.py"""
import importlib as 가져오기
import sys as ऑपरेटिंग_सिस्टम_मान
from pathlib import Path as पथ
ऑपरेटिंग_सिस्टम_मान.path.insert(0, str(पथ(__file__).resolve().parents[1] / 'उपकरण'))
if __name__ == '__main__':
    import runpy as ऐप_लॉन्चर
    ऐप_लॉन्चर.run_module('बिल्ड_सी_कंपाइलर', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('बिल्ड_सी_कंपाइलर')
    대응 = {'out': 'परिणाम_डेटा', 'builtins': '내장연산', 'header': 'हेडर_मान', 'sdk': 'डेवलपमेंट_किट', 'build_ccompiler': 'बनाएँ_सी_कंपाइलर', 'i': '순번', 'elf': 'निष्पादन_योग्य_फ़ाइल', 'run': 'निष्पादित_करें_आदेश', 'flags': 'कॉन्फ़िगरेशन_बैकग्राउंड_इंटेलिजेंट_ट्रांसफ़र_सर्विस', 'path': 'पथ', 'p': 'डेटा_पद', 'cc': 'सी_कंपाइलर', 'obj': 'गंतव्य_फ़ाइल', 'flag': 'सेटिंग_मान', 'ld': '연결편집기', 'objects': 'गंतव्य_फ़ाइलें', 'repo': 'संग्रह_पथ', 'v': '임시값', 'upstream': 'अपस्ट्रीम', 'root': 'मूल_पता', 'assets': '탑재자료', 'source': '원본자료', 'name': 'नाम', 'includes': '포함인수'}
    for 이전, अद्यतित_आइटम in 대응.items():
        if hasattr(구현, अद्यतित_आइटम): globals()[이전] = getattr(구현, अद्यतित_आइटम)
