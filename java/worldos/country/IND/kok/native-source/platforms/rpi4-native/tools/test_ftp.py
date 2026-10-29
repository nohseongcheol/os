#!/usr/bin/env python3
"""기존 पाथ 호환 प्रवेश_पॉयंट. प्रत्यक्ष_डेटा 구현: ../साधनां/파일전송시험.py"""
import importlib as TAKE_मोल
import sys as ऑपरेटिंग_प्रणाली_मोल
from pathlib import Path as पाथ
ऑपरेटिंग_प्रणाली_मोल.path.insert(0, str(पाथ(__file__).resolve().parents[1] / 'साधनां'))
if __name__ == '__main__':
    import runpy as एप्लिकेशन_ऍप्लिकेशन_ड्रॉवर
    एप्लिकेशन_ऍप्लिकेशन_ड्रॉवर.run_module('파일전송시험', run_name='__main__', alter_sys=True)
else:
    구현 = TAKE_मोल.import_module('파일전송시험')
    대응 = {'timeout': '시간제한', 'payload': 'पेलोड_डेटा', 'broken': '손상자료', 'linux_example': '리눅스예제', 'chunk': '조각', 'data': 'डेटा', 'proc': 'प्रक्रिया', 'code': 'समजावणी_SEQUENCE', 'linux': '리눅스파일', 'archive': 'संग्रह', 'main': 'चलोवप', 'net_source': '통신원문', 'temporary': '임시자원', 'static_source': 'थीर_स्त्रोत', 'java_source': '자바원문', 'echo': '되돌림서버항목', 'ROOT': 'प्रॉजॅक्ट_रूट', 'text': 'SMS', 'marker': '확인표시', 'EchoFixture': '되돌림시험서버', 'command': 'आदेश', 'out': 'मेजप_डेटा', 'expected': '예상결과', 'server_source': 'सर्वर_स्त्रोत', 'shell': 'शॅल', 'upload': 'अपलोड_करचें_फायली', 'transcript': '대화기록', 'port': '접속번호', 'native': '자체실행파일', 'elf': '실행파일', 'server_udp_port': '서버전문접속번호', 'packed': '묶인자료', 'bridge': 'ब्रिज', 'selector': 'वेंचक', 'end': 'सोपोवचें_ऑफसॅट', 'e': '보조항목', 'ftp': 'फायल_ट्रान्सफर_कनॅक्शन', 'key': '누름값', 'bytecode': '바이트코드', 'peer': 'पीयर_मोल', 'result': 'मेजप', 'unchanged': '보존자료', 'line': 'रेग', 'server_tcp_port': 'सर्वर_Stream_पोर्ट', 'source': '원본자료', 'NetworkBridge': 'नॅटवर्क_ब्रिज', 'jar': '자바꾸러미', 'receive': '수신하기', 'report': 'वैधताय_अहवाल'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
