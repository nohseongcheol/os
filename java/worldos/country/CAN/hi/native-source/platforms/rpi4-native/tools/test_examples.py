#!/usr/bin/env python3
"""기존 पथ 호환 प्रवेश_बिदुं. वास्तविक_डेटा 구현: ../उपकरण/예제시험.py"""
import importlib as 가져오기
import sys as ऑपरेटिंग_सिस्टम_मान
from pathlib import Path as पथ
ऑपरेटिंग_सिस्टम_मान.path.insert(0, str(पथ(__file__).resolve().parents[1] / 'उपकरण'))
if __name__ == '__main__':
    import runpy as ऐप_लॉन्चर
    ऐप_लॉन्चर.run_module('예제시험', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('예제시험')
    대응 = {'count': '항목수', 'exact': '정확한값', 'expected_file': '예상파일', 'ftp_port': 'फ़ाइल_स्थानांतरण_पोर्ट_संख्या', 'data': 'आँकड़े', 'graphics_command': 'ग्राफ़िक्स_आदेश', 'main': 'चलाएँ', 'row': 'पंक्ति_पद', 'init': '초기값', 'target': 'लक्ष्य', 'ROOT': 'प्रोजेक्ट_करें_मूल', 'text': 'पाठ', 'binary': 'बाइनरी', 'out': 'परिणाम_डेटा', 'entry': 'प्रवेश_बिदुं', 'got': '받은수', 'port': 'पोर्ट_संख्या', 'graphics_start': 'प्रारंभ_ड्रॉइंग', 'col': 'कालम_पद', 'begin': 'प्रारंभ_ऑफ़सेट', 'kind': 'श्रेणी_मान', 'selector': 'सिलेक्टर', 'n': '개수', 'key': '누름값', 'y': '세로좌표', 'client': 'क्लायंट', 'line': 'पंक्ति', 'report': 'प्रमाणीकरण_रिपोर्ट', 'language': 'भाषा', 'x': 'x_निर्देशांक', 'start': 'चलाएँ', 'rgb': '빛삼원색', 'down': '누르는중', 'listing': 'भेजें_सूची', 'payload': 'पेलोड_डेटा', 'proc': 'प्रक्रिया', 'w': '너비값', 'temporary': '임시자원', 'echo': '되돌림서버항목', 'label': 'नाम_तालिका', 'content': 'सामग्री_मान', 'argument': '전달값', 'EchoServers': 'प्रतिध्वनि_सर्वर', 'marker': 'मार्कर', 'expected': '예상결과', 'test_language': 'test_언어', 'filename': 'फ़ाइल_एन्ट्री_नाम', 'shell': 'शेल', 'color': '색상', 'transcript': 'बोला_गया_पाठ', 'offset': 'ऑफ़सेट_मान', 'h': '높이값', 'run': 'निष्पादित_करें_आदेश', 'c': 'वर्ण_कोड', 'path': 'पथ', 'encoding': 'वर्ण_सेट', 'end': 'समाप्त_करें_ऑफ़सेट', 'ftp': 'फ़ाइल_स्थानांतरण_कनेक्शन', 'pixels': '화소들', 'symbol': 'प्रतीक_मान', 'source': '원본자료', 'name': 'नाम', 'receive': '수신하기', 'manifest': 'बंडल_सूची'}
    for 이전, अद्यतित_आइटम in 대응.items():
        if hasattr(구현, अद्यतित_आइटम): globals()[이전] = getattr(구현, अद्यतित_आइटम)
