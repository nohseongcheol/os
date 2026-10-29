#!/usr/bin/env python3
"""기존 पथ 호환 प्रवेश_बिदुं. वास्तविक_डेटा 구현: ../उपकरण/डेस्कटॉप_दृश्य.py"""
import importlib as 가져오기
import sys as ऑपरेटिंग_सिस्टम_मान
from pathlib import Path as पथ
ऑपरेटिंग_सिस्टम_मान.path.insert(0, str(पथ(__file__).resolve().parents[1] / 'उपकरण'))
if __name__ == '__main__':
    import runpy as ऐप_लॉन्चर
    ऐप_लॉन्चर.run_module('डेस्कटॉप_दृश्य', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('डेस्कटॉप_दृश्य')
    대응 = {'count': '항목수', 'special': '특수글쇠', 'error': 'त्रुटि', 'exact': '정확한값', 'network': 'नेटवर्क', 'closed': '닫힘', 'length': '길이', 'opened': '열림', 'ftp_port': 'फ़ाइल_स्थानांतरण_पोर्ट_संख्या', 'server': '서버', 'resources': 'संसाधन', 'data': 'आँकड़े', 'shift': 'SHIFT_कुंजी', 'send': 'भेजें', 'run_desktop': 'चलाएँ_डेस्कटॉप', 'protocol': '통신규약', 'forwards': '전달규칙들', 'host': 'आयोजक', 'text': 'पाठ', 'korean': '한글여부', 'port': 'पोर्ट_संख्या', 'signum': '신호번호', 'version': 'संस्करण_संख्या', 'parser': 'पार्सर', 'bridge': 'ब्रिज', 'kind': 'श्रेणी_मान', 'tail': '끝부분', 'size': 'आकार', 'previous_buttons': '이전단추', 'key': '누름값', 'y': '세로좌표', 'prefix': '앞부분', 'client': 'क्लायंट', 'char': 'वर्ण_डेटा', 'work': '작업경로', 'Keyboard': 'कीबोर्ड', 'x': 'x_निर्देशांक', 'down': '누르는중', 'net': 'ब्रिज_एन्ट्री', 'self': '자신', 'mode_changed': '입력방식알림', 'serial': '직렬입출력', 'args': 'तर्क_सरणी', 'Hangul': '한글조합', 'chunk': '조각', 'proc': 'प्रक्रिया', 'Desktop': 'कनेक्ट_डेस्कटॉप', 'buttons': '단추들', 'thread': 'कार्यसूत्र', 'pressed': '눌림', 'previous': '이전항목', 'toggle': 'स्विच_मोड', 'command': 'आदेश', 'sock': 'सॉकेट_मान', 'frame': '실행틀', 'ctrl': 'नियंत्रण_कुंजी', 'path': 'पथ', 'cp': 'वर्ण_एन्_कोडिंग', 'terminate': 'पर्यवसान', 'security': 'सुरक्षा', 'vnc_port': '원격화면접속번호', 'body': 'मुख्य_पाठ', 'index': 'लुकअप_इंडेक्स', 'exited': '종료됨', 'keysym': 'कुंजी_प्रतीक', 'output': '출력결과', 'keyboard': 'कीबोर्ड_एन्ट्री', 'interrupted': '가로채기됨', 'listener': '수신창구', 'reader': 'पाठक', 'NetworkBridge': 'ब्रिज_3de4fe3a', 'gui': '그림화면', 'worker': 'संसाधन_कार्य'}
    for 이전, अद्यतित_आइटम in 대응.items():
        if hasattr(구현, अद्यतित_आइटम): globals()[이전] = getattr(구현, अद्यतित_आइटम)
