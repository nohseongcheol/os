#!/usr/bin/env python3
"""기존 पथ 호환 प्रवेश_बिदुं. वास्तविक_डेटा 구현: ../उपकरण/원격한글시험.py"""
import importlib as 가져오기
import sys as ऑपरेटिंग_सिस्टम_मान
from pathlib import Path as पथ
ऑपरेटिंग_सिस्टम_मान.path.insert(0, str(पथ(__file__).resolve().parents[1] / 'उपकरण'))
if __name__ == '__main__':
    import runpy as ऐप_लॉन्चर
    ऐप_लॉन्चर.run_module('원격한글시험', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('원격한글시험')
    대응 = {'wait': '기다리기', 'typing': '글자입력', 'start': 'चलाएँ', 'profile': 'प्रोफ़ाइल', 'focused': 'केंद्रित', 'serial': '직렬입출력', 'keys': '누름열', 'server': '서버', 'log': 'लॉग_रिकॉर्ड', 'args': 'तर्क_सरणी', 'deadline': 'अंति_म_समय_सीमा_समय', 'data': 'आँकड़े', 'candidate': '후보', 'logs': '기록들', 'kw': 'नामित_तर्क', 'number': '수치', 'main': 'चलाएँ', 'ready': '준비완료', 'found': 'खोज_परिणाम', 'guest': 'अतिथि', 'ROOT': 'प्रोजेक्ट_करें_मूल', 'marker': 'मार्कर', 'text': 'पाठ', 'out': 'परिणाम_डेटा', 'env': '환경', 'f': 'फ़ाइल_एन्ट्री', 'port': 'पोर्ट_संख्या', 'offset': 'ऑफ़सेट_मान', 'version': 'संस्करण_संख्या', 'p': 'डेटा_पद', 'selector': 'सिलेक्टर', 'xvfb': '가상표시장치', 'display': 'डिस्प्ले', 'n': '개수', 'key': '누름값', 'processes': '실행과정들', 'rootfs': '뿌리파일계층', 'xdo': '가상입력도구', 'name': 'नाम', 'window': 'खिड़की', 'report': 'प्रमाणीकरण_रिपोर्ट', 'work': '작업경로'}
    for 이전, अद्यतित_आइटम in 대응.items():
        if hasattr(구현, अद्यतित_आइटम): globals()[이전] = getattr(구현, अद्यतित_आइटम)
