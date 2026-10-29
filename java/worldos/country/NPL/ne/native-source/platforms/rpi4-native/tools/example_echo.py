#!/usr/bin/env python3
"""기존 मार्ग 호환 प्रविष्टि_अंक. वास्तविक_लगत 구현: ../उपकरणहरू/예제되돌림서버.py"""
import importlib as 가져오기
import sys as सञ्चालनप्रणाली_मान
from pathlib import Path as मार्ग
सञ्चालनप्रणाली_मान.path.insert(0, str(मार्ग(__file__).resolve().parents[1] / 'उपकरणहरू'))
if __name__ == '__main__':
    import runpy as अनुप्रयोग_कर्मचारी_अगुवा
    अनुप्रयोग_कर्मचारी_अगुवा.run_module('예제되돌림서버', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('예제되돌림서버')
    대응 = {'data': 'लगत', 'sock': '소켓', 'tcp_port': 'टिसिपी_पोर्ट', 'chunk': '조각', 'received': '수신됨', 'self': '자신', 'UDP': '전문요청처리', 'thread': '작업가닥', 'echo': '되돌림서버항목', 'TCP': '연결요청처리', 'EchoServers': '되돌림서버', 'parser': '인수해석기', 'server': 'सर्भर_मान', 'udp_port': 'युडिपी_पोर्ट', 'args': 'तर्क_विन्यास'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
