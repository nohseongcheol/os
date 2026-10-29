#!/usr/bin/env python3
"""기존 पाथ 호환 प्रवेश_पॉयंट. प्रत्यक्ष_डेटा 구현: ../साधनां/예제되돌림서버.py"""
import importlib as TAKE_मोल
import sys as ऑपरेटिंग_प्रणाली_मोल
from pathlib import Path as पाथ
ऑपरेटिंग_प्रणाली_मोल.path.insert(0, str(पाथ(__file__).resolve().parents[1] / 'साधनां'))
if __name__ == '__main__':
    import runpy as एप्लिकेशन_ऍप्लिकेशन_ड्रॉवर
    एप्लिकेशन_ऍप्लिकेशन_ड्रॉवर.run_module('예제되돌림서버', run_name='__main__', alter_sys=True)
else:
    구현 = TAKE_मोल.import_module('예제되돌림서버')
    대응 = {'data': 'डेटा', 'sock': '소켓', 'tcp_port': 'TCP_पोर्ट', 'chunk': '조각', 'received': '수신됨', 'self': '자신', 'UDP': '전문요청처리', 'thread': '작업가닥', 'echo': '되돌림서버항목', 'TCP': '연결요청처리', 'EchoServers': '되돌림서버', 'parser': '인수해석기', 'server': 'सर्वर_मोल', 'udp_port': 'UDP_पोर्ट', 'args': 'युक्तीवाद_क्रम'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
