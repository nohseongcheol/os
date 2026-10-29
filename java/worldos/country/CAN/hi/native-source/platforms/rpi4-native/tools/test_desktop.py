#!/usr/bin/env python3
"""기존 पथ 호환 प्रवेश_बिदुं. वास्तविक_डेटा 구현: ../उपकरण/바탕화면시험.py"""
import importlib as 가져오기
import sys as ऑपरेटिंग_सिस्टम_मान
from pathlib import Path as पथ
ऑपरेटिंग_सिस्टम_मान.path.insert(0, str(पथ(__file__).resolve().parents[1] / 'उपकरण'))
if __name__ == '__main__':
    import runpy as ऐप_लॉन्चर
    ऐप_लॉन्चर.run_module('바탕화면시험', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('바탕화면시험')
    대응 = {'x': 'x_निर्देशांक', 'typing': '글자입력', 'message': 'सूचना_पाठ', 'start': 'चलाएँ', 'down': '누르는중', 'exact': '정확한값', 'i': '순번', 'press': 'दबाएँ_कुंजी', 'rectangles': '사각형들', 'sym': 'प्रतीक', 'j': '안쪽순번', 'deadline': 'अंति_म_समय_सीमा_समय', 'proc': 'प्रक्रिया', 'data': 'आँकड़े', 'main': 'चलाएँ', 'w': '너비값', 'init': '초기값', 'block': 'डेटा_ब्_लॉक', 'ROOT': 'प्रोजेक्ट_करें_मूल', 'text': 'पाठ', 'marker': 'मार्कर', 'report': 'प्रमाणीकरण_रिपोर्ट', 'until': '까지', 'clipboard': 'क्लिपबोर्ड_मान', 'dst': 'गंतव्य_पता', 'seen': '본항목들', 'poll': 'तैयारी_मॉनीटर', 'transcript': 'बोला_गया_पाठ', 'port': 'पोर्ट_संख्या', 'offset': 'ऑफ़सेट_मान', 'h': '높이값', 'src': '원본주소', 'event': 'घटना', 'encoding': 'वर्ण_सेट', 'size': 'आकार', 'key': '누름값', 'pixels': '화소들', 'y': '세로좌표', 'output': '출력결과', 'symbol': 'प्रतीक_मान', 'client': 'क्लायंट', 'char': 'वर्ण_डेटा', 'rgb': '빛삼원색'}
    for 이전, अद्यतित_आइटम in 대응.items():
        if hasattr(구현, अद्यतित_आइटम): globals()[이전] = getattr(구현, अद्यतित_आइटम)
