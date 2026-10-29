#!/usr/bin/env python3
"""기존 पथ 호환 प्रवेश_बिदुं. वास्तविक_डेटा 구현: ../उपकरण/ब्रिज_3de4fe3a.py"""
import importlib as 가져오기
import sys as ऑपरेटिंग_सिस्टम_मान
from pathlib import Path as पथ
ऑपरेटिंग_सिस्टम_मान.path.insert(0, str(पथ(__file__).resolve().parents[1] / 'उपकरण'))
if __name__ == '__main__':
    import runpy as ऐप_लॉन्चर
    ऐप_लॉन्चर.run_module('ब्रिज_3de4fe3a', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('ब्रिज_3de4fe3a')
    대응 = {'response': 'प्रतिसाद', 'parts': 'पथ_घटक', 's': 'स्ट्रिंग_डेटा', 'i': '순번', 'close': 'बंदकरें', 'forward': '전달규칙', 'slip_input': '직렬전문입력', 'self': '자신', 'item': 'एन्ट्री_मान', 'flags': 'कॉन्फ़िगरेशन_बैकग्राउंड_इंटेलिजेंट_ट्रांसफ़र_सर्विस', 'ftp_port': 'फ़ाइल_स्थानांतरण_पोर्ट_संख्या', 'args': 'तर्क_सरणी', 'server': '서버', 'data': 'आँकड़े', 'ethernet_input': '이더넷입력', 'trace_packet': 'ट्रेस_पैकेट', 'GATEWAY': '관문기계주소', 'rule': 'नियम_मान', 'protocol': '통신규약', 'forwards': '전달규칙들', 'occupied': '사용중주소', 'host': 'आयोजक', 'ack': '확인번호', 'serial_port': '직렬접속번호', 'readers': '읽기대상들', 'guest': 'अतिथि', 'destination': 'गंतव्य_डेटा_पता', 'ethernet_port': 'ईथरनेट_पोर्ट', 'b': '둘째값', 'MAC': 'वास्तविक_पता', 'arp': 'पता_रिज़ॉल्यूशन_पैकेट', 'writable': '쓸수있음', 'direction': '방향', 'seq': '순서번호', 'frame': '실행틀', 'loop': 'चक्र_मान', 'port': 'पोर्ट_संख्या', 'offset': 'ऑफ़सेट_मान', 'readable': '읽을수있음', 'c': 'वर्ण_कोड', 'p': 'डेटा_पद', 'writers': '쓰기대상들', 'IP': 'इंटरनेट_पता_मान', 'e': '보조항목', 'n': '개수', 'packet': 'पैकेट_डेटा', 'arguments': '전달인수', 'source': '원본자료', 'NetworkBridge': 'ब्रिज_3de4fe3a', 'window': 'खिड़की', 'capture': 'कैप्चर_करें'}
    for 이전, अद्यतित_आइटम in 대응.items():
        if hasattr(구현, अद्यतित_आइटम): globals()[이전] = getattr(구현, अद्यतित_आइटम)
