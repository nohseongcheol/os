#!/usr/bin/env python3
"""기존 पथ 호환 प्रवेश_बिदुं. वास्तविक_डेटा 구현: ../उपकरण/셸시험.py"""
import importlib as 가져오기
import sys as ऑपरेटिंग_सिस्टम_मान
from pathlib import Path as पथ
ऑपरेटिंग_सिस्टम_मान.path.insert(0, str(पथ(__file__).resolve().parents[1] / 'उपकरण'))
if __name__ == '__main__':
    import runpy as ऐप_लॉन्चर
    ऐप_लॉन्चर.run_module('셸시험', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('셸시험')
    대응 = {'timeout': '시간제한', 'x': 'x_निर्देशांक', 'msg': 'नेटवर्क_ईमेल', 'i': '순번', 'reply': 'उत्तर', 'call': '호출', 'args': 'तर्क_सरणी', 'chunk': '조각', 'data': 'आँकड़े', 'proc': 'प्रक्रिया', 'long_text': '긴글', 'restored': '복원자료', 'send': 'भेजें', 'file': 'संचिका', 'main': 'चलाएँ', 'found': 'खोज_परिणाम', 'ROOT': 'प्रोजेक्ट_करें_मूल', 'text': 'पाठ', 'marker': 'मार्कर', 'command': 'आदेश', 'expected': '예상결과', 'pixel': 'पिक्सेल', 'shell': 'शेल', 'poll': 'तैयारी_मॉनीटर', 'transcript': 'बोला_गया_पाठ', 'end': 'समाप्त_करें_ऑफ़सेट', 'image': 'छवि', 'key': '누름값', 'y': '세로좌표', 'output': '출력결과', 'result': 'परिणाम', 'client': 'क्लायंट', 'line': 'पंक्ति', 'stream': 'स्ट्रीम_मान', 'name': 'नाम', 'value': 'मान', 'receive': '수신하기', 'report': 'प्रमाणीकरण_रिपोर्ट', 'work': '작업경로', 'qmp': '모의제어접속'}
    for 이전, अद्यतित_आइटम in 대응.items():
        if hasattr(구현, अद्यतित_आइटम): globals()[이전] = getattr(구현, अद्यतित_आइटम)
