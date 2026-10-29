#!/usr/bin/env python3
"""기존 पथ 호환 प्रवेश_बिदुं. वास्तविक_डेटा 구현: ../उपकरण/부팅시험.py"""
import importlib as 가져오기
import sys as ऑपरेटिंग_सिस्टम_मान
from pathlib import Path as पथ
ऑपरेटिंग_सिस्टम_मान.path.insert(0, str(पथ(__file__).resolve().parents[1] / 'उपकरण'))
if __name__ == '__main__':
    import runpy as ऐप_लॉन्चर
    ऐप_लॉन्चर.run_module('부팅시험', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('부팅시험')
    대응 = {'timeout': '시간제한', 'response': 'प्रतिसाद', 'msg': 'नेटवर्क_ईमेल', 'exact': '정확한값', 'markers': '확인표시들', 'i': '순번', 'match': '일치', 'execute': 'निष्पादन', 'cancel': 'रद्द_करें_ऑपरेशन', 'cmd_byte': 'आदेश_बाइट', 'reply': 'उत्तर', 'points': '지점들', 'server': '서버', 'data': 'आँकड़े', 'prompt': 'संकेत', 'enter': 'दर्ज_करें', 'imported': '들여온파일', 'send': 'भेजें', 'main': 'चलाएँ', 'ROOT': 'प्रोजेक्ट_करें_मूल', 'text': 'पाठ', 'first_gui': '첫화면', 'pixel': 'पिक्सेल', 'java_class': '자바클래스', 'upload': 'अपलोड_फ़ाइलें', 'pixels_file': 'पिक्सेल_फ़ाइल', 'pixels_data': 'पिक्सेल_डेटा', 'edit': 'संपादन_मान', 'receive_until': '표시까지받기', 'selector': 'सिलेक्टर', 'size': 'आकार', 'qmp_path': '모의제어경로', 'key': '누름값', 'second_gui': '둘째화면', 'y': '세로좌표', 'result': 'परिणाम', 'samples': '예제들', 'client': 'क्लायंट', 'line': 'पंक्ति', 'report': 'प्रमाणीकरण_रिपोर्ट', 'work': '작업경로', 'x': 'x_निर्देशांक', 'python_checks': '파이썬검사', 'download': 'डाउनलोड', 'greeting': 'अभिनन्दन_ae353e94', 'dims': '치수', 'chunk': '조각', 'deadline': 'अंति_म_समय_सीमा_समय', 'proc': 'प्रक्रिया', 'content': 'सामग्री_मान', 'block': 'डेटा_ब्_लॉक', 'marker': 'मार्कर', 'command': 'आदेश', 'expected': '예상결과', 'shell': 'शेल', 'drawing': 'ड्रॉइंग_पथ', 'f': 'फ़ाइल_एन्ट्री', 'transcript': 'बोला_गया_पाठ', 'offset': 'ऑफ़सेट_मान', 'path': 'पथ', 'screenshot': 'स्क्रीनशॉट', 'arguments': '전달인수', 'pixels': '화소들', 'viewer': '화면접속자', 'output': '출력결과', 'stream': 'स्ट्रीम_मान', 'cmd': '명령인수', 'name': 'नाम', 'qmp': '모의제어접속'}
    for 이전, अद्यतित_आइटम in 대응.items():
        if hasattr(구현, अद्यतित_आइटम): globals()[이전] = getattr(구현, अद्यतित_आइटम)
