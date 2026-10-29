#!/usr/bin/env python3
"""기존 पाथ 호환 प्रवेश_पॉयंट. प्रत्यक्ष_डेटा 구현: ../साधनां/नॅटवर्क_ब्रिज.py"""
import importlib as TAKE_मोल
import sys as ऑपरेटिंग_प्रणाली_मोल
from pathlib import Path as पाथ
ऑपरेटिंग_प्रणाली_मोल.path.insert(0, str(पाथ(__file__).resolve().parents[1] / 'साधनां'))
if __name__ == '__main__':
    import runpy as एप्लिकेशन_ऍप्लिकेशन_ड्रॉवर
    एप्लिकेशन_ऍप्लिकेशन_ड्रॉवर.run_module('नॅटवर्क_ब्रिज', run_name='__main__', alter_sys=True)
else:
    구현 = TAKE_मोल.import_module('नॅटवर्क_ब्रिज')
    대응 = {'response': '응답자료', 'parts': 'पाथ_घटक', 's': 'स्ट्रिंग_डेटा', 'i': '순번', 'close': 'शेवट', 'forward': '전달규칙', 'slip_input': '직렬전문입력', 'self': '자신', 'item': 'प्रवेश_मोल', 'flags': '설정비트', 'ftp_port': '파일전송접속번호', 'args': 'युक्तीवाद_क्रम', 'server': 'सर्वर_मोल', 'data': 'डेटा', 'ethernet_input': '이더넷입력', 'trace_packet': '전문추적', 'GATEWAY': 'गेटवे_हार्डवॅर_नामो', 'rule': 'नेम_मोल', 'protocol': '통신규약', 'forwards': '전달규칙들', 'occupied': '사용중주소', 'host': 'येजमान', 'ack': '확인번호', 'serial_port': '직렬접속번호', 'readers': '읽기대상들', 'guest': 'सोयरो', 'destination': 'नियुक्त_स्थान_डेटा_नामो', 'ethernet_port': 'इथरनॅट_पोर्ट', 'b': 'SECOND_मोल', 'MAC': 'यंत्र_नामो', 'arp': 'नामो_रिजोल्युशन_पॅकेट', 'writable': '쓸수있음', 'direction': '방향', 'seq': '순서번호', 'frame': '실행틀', 'loop': 'सायकल_मोल', 'port': '접속번호', 'offset': 'ऑफसॅट_मोल', 'readable': '읽을수있음', 'c': 'वर्ण_कोड', 'p': 'डेटा_स्थिती', 'writers': '쓰기대상들', 'IP': 'माजाळ्याचो_नामो_मोल', 'e': '보조항목', 'n': 'आयटम_COUNT', 'packet': 'पॅकेट_डेटा', 'arguments': '전달인수', 'source': '원본자료', 'NetworkBridge': 'नॅटवर्क_ब्रिज', 'window': 'विंडो', 'capture': 'कॅप्चर'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
