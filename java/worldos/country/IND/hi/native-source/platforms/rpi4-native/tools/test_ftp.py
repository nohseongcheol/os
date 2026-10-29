#!/usr/bin/env python3
"""기존 पथ 호환 प्रवेश_बिदुं. वास्तविक_डेटा 구현: ../उपकरण/파일전송시험.py"""
import importlib as 가져오기
import sys as ऑपरेटिंग_सिस्टम_मान
from pathlib import Path as पथ
ऑपरेटिंग_सिस्टम_मान.path.insert(0, str(पथ(__file__).resolve().parents[1] / 'उपकरण'))
if __name__ == '__main__':
    import runpy as ऐप_लॉन्चर
    ऐप_लॉन्चर.run_module('파일전송시험', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('파일전송시험')
    대응 = {'timeout': '시간제한', 'payload': 'पेलोड_डेटा', 'broken': '손상자료', 'linux_example': '리눅스예제', 'chunk': '조각', 'data': 'आँकड़े', 'proc': 'प्रक्रिया', 'code': '명령열', 'linux': '리눅스파일', 'archive': 'संग्रह', 'main': 'चलाएँ', 'net_source': '통신원문', 'temporary': '임시자원', 'static_source': '정적원문', 'java_source': '자바원문', 'echo': '되돌림서버항목', 'ROOT': 'प्रोजेक्ट_करें_मूल', 'text': 'पाठ', 'marker': 'मार्कर', 'EchoFixture': '되돌림시험서버', 'command': 'आदेश', 'out': 'परिणाम_डेटा', 'expected': '예상결과', 'server_source': '서버원문', 'shell': 'शेल', 'upload': 'अपलोड_फ़ाइलें', 'transcript': 'बोला_गया_पाठ', 'port': 'पोर्ट_संख्या', 'native': '자체실행파일', 'elf': 'निष्पादन_योग्य_फ़ाइल', 'server_udp_port': '서버전문접속번호', 'packed': '묶인자료', 'bridge': 'ब्रिज', 'selector': 'सिलेक्टर', 'end': 'समाप्त_करें_ऑफ़सेट', 'e': '보조항목', 'ftp': 'फ़ाइल_स्थानांतरण_कनेक्शन', 'key': '누름값', 'bytecode': '바이트코드', 'peer': 'पीअर_मान', 'result': 'परिणाम', 'unchanged': '보존자료', 'line': 'पंक्ति', 'server_tcp_port': '서버연결접속번호', 'source': '원본자료', 'NetworkBridge': 'ब्रिज_3de4fe3a', 'jar': '자바꾸러미', 'receive': '수신하기', 'report': 'प्रमाणीकरण_रिपोर्ट'}
    for 이전, अद्यतित_आइटम in 대응.items():
        if hasattr(구현, अद्यतित_आइटम): globals()[이전] = getattr(구현, अद्यतित_आइटम)
