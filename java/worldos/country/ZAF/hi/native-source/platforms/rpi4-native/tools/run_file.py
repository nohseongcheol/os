#!/usr/bin/env python3
"""기존 पथ 호환 प्रवेश_बिदुं. वास्तविक_डेटा 구현: ../उपकरण/निष्पादित_करें_फ़ाइल.py"""
import importlib as 가져오기
import sys as ऑपरेटिंग_सिस्टम_मान
from pathlib import Path as पथ
ऑपरेटिंग_सिस्टम_मान.path.insert(0, str(पथ(__file__).resolve().parents[1] / 'उपकरण'))
if __name__ == '__main__':
    import runpy as ऐप_लॉन्चर
    ऐप_लॉन्चर.run_module('निष्पादित_करें_फ़ाइल', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('निष्पादित_करें_फ़ाइल')
    대응 = {'timeout': '시간제한', 's': 'स्ट्रिंग_डेटा', 'i': '순번', 'match': '일치', 'files': 'फ़ाइल_सूची', 'program': 'ऐप', 'executable': 'निष्पादन_योग्य_फ़ाइल_छवि', 'args': 'तर्क_सरणी', 'chunk': '조각', 'data': 'आँकड़े', 'proc': 'प्रक्रिया', 'send': 'भेजें', 'main': 'चलाएँ', 'marker': 'मार्कर', 'command': 'आदेश', 'include': '포함항목', 'dumped': '갈무리자료', 'run': 'निष्पादित_करें_आदेश', 'p': 'डेटा_पद', 'parser': 'पार्सर', 'options': 'विकल्प', 'kind': 'श्रेणी_मान', 'selector': 'सिलेक्टर', 'upload_data': 'अपलोड_डेटा', 'end': 'समाप्त_करें_ऑफ़सेट', 'n': '개수', 'd': 'गंतव्य_डेटा', 'key': '누름값', 'output': '출력결과', 'line': 'पंक्ति', 'name': 'नाम', 'upload_name': 'अपलोड_नाम', 'receive': '수신하기'}
    for 이전, अद्यतित_आइटम in 대응.items():
        if hasattr(구현, अद्यतित_आइटम): globals()[이전] = getattr(구현, अद्यतित_आइटम)
