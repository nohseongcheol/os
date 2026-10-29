#!/usr/bin/env python3
"""기존 पथ 호환 प्रवेश_बिदुं. वास्तविक_डेटा 구현: ../उपकरण/예제되돌림서버.py"""
import importlib as 가져오기
import sys as ऑपरेटिंग_सिस्टम_मान
from pathlib import Path as पथ
ऑपरेटिंग_सिस्टम_मान.path.insert(0, str(पथ(__file__).resolve().parents[1] / 'उपकरण'))
if __name__ == '__main__':
    import runpy as ऐप_लॉन्चर
    ऐप_लॉन्चर.run_module('예제되돌림서버', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('예제되돌림서버')
    대응 = {'data': 'आँकड़े', 'sock': 'सॉकेट_मान', 'tcp_port': '연결접속번호', 'chunk': '조각', 'received': '수신됨', 'self': '자신', 'UDP': '전문요청처리', 'thread': 'कार्यसूत्र', 'echo': '되돌림서버항목', 'TCP': 'हैंडल_कनेक्शन_अनुरोध', 'EchoServers': 'प्रतिध्वनि_सर्वर', 'parser': 'पार्सर', 'server': '서버', 'udp_port': 'यूज़र_डेटाग्राम_प्रॉटोकॉल_पोर्ट', 'args': 'तर्क_सरणी'}
    for 이전, अद्यतित_आइटम in 대응.items():
        if hasattr(구현, अद्यतित_आइटम): globals()[이전] = getattr(구현, अद्यतित_आइटम)
