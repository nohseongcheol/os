#!/usr/bin/env python3
"""기존 मार्ग 호환 प्रविष्टि_अंक. वास्तविक_लगत 구현: ../उपकरणहरू/सञ्जाल_ब्रिज.py"""
import importlib as 가져오기
import sys as सञ्चालनप्रणाली_मान
from pathlib import Path as मार्ग
सञ्चालनप्रणाली_मान.path.insert(0, str(मार्ग(__file__).resolve().parents[1] / 'उपकरणहरू'))
if __name__ == '__main__':
    import runpy as अनुप्रयोग_कर्मचारी_अगुवा
    अनुप्रयोग_कर्मचारी_अगुवा.run_module('सञ्जाल_ब्रिज', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('सञ्जाल_ब्रिज')
    대응 = {'response': '응답자료', 'parts': 'बाटो_घटक', 's': 'स्ट्रिङ_लगत', 'i': '순번', 'close': 'बन्दगर्नुहोस्', 'forward': '전달규칙', 'slip_input': '직렬전문입력', 'self': '자신', 'item': 'प्रविष्टि_मान', 'flags': '설정비트', 'ftp_port': '파일전송접속번호', 'args': 'तर्क_विन्यास', 'server': 'सर्भर_मान', 'data': 'लगत', 'ethernet_input': '이더넷입력', 'trace_packet': '전문추적', 'GATEWAY': 'गेटवे_हार्डवेयर_ठेगाना', 'rule': 'नियम_मान', 'protocol': '통신규약', 'forwards': '전달규칙들', 'occupied': '사용중주소', 'host': 'होस्ट', 'ack': '확인번호', 'serial_port': '직렬접속번호', 'readers': '읽기대상들', 'guest': 'अतिथि', 'destination': 'गन्तव्य_लगत_ठेगाना', 'ethernet_port': 'इथरनेट_पोर्ट', 'b': '둘째값', 'MAC': 'मेशिन_ठेगाना', 'arp': 'ठेगाना_रिजोल्यूशन_प्याकेट', 'writable': '쓸수있음', 'direction': '방향', 'seq': '순서번호', 'frame': '실행틀', 'loop': 'चक्र_मान', 'port': '접속번호', 'offset': 'अफसेट_मान', 'readable': '읽을수있음', 'c': 'वर्ण_सङ्केत', 'p': 'लगत_राख्नुहोस्', 'writers': '쓰기대상들', 'IP': 'इन्टरनेट_ठेगाना_मान', 'e': '보조항목', 'n': '개수', 'packet': 'प्याकेट_लगत', 'arguments': '전달인수', 'source': '원본자료', 'NetworkBridge': 'सञ्जाल_ब्रिज', 'window': 'सन्झ्याल', 'capture': 'क्यापचर'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
