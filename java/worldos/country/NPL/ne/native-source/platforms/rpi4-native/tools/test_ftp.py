#!/usr/bin/env python3
"""기존 मार्ग 호환 प्रविष्टि_अंक. वास्तविक_लगत 구현: ../उपकरणहरू/파일전송시험.py"""
import importlib as 가져오기
import sys as सञ्चालनप्रणाली_मान
from pathlib import Path as मार्ग
सञ्चालनप्रणाली_मान.path.insert(0, str(मार्ग(__file__).resolve().parents[1] / 'उपकरणहरू'))
if __name__ == '__main__':
    import runpy as अनुप्रयोग_कर्मचारी_अगुवा
    अनुप्रयोग_कर्मचारी_अगुवा.run_module('파일전송시험', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('파일전송시험')
    대응 = {'timeout': '시간제한', 'payload': 'पेलोड_लगत', 'broken': '손상자료', 'linux_example': '리눅스예제', 'chunk': '조각', 'data': 'लगत', 'proc': 'प्रक्रिया', 'code': '명령열', 'linux': '리눅스파일', 'archive': 'सङ्ग्रह', 'main': 'चलाउनुहोस्', 'net_source': '통신원문', 'temporary': '임시자원', 'static_source': 'तथ्याङ्कित_स्रोत', 'java_source': '자바원문', 'echo': '되돌림서버항목', 'ROOT': 'परियोजना_रूट', 'text': 'पाठ', 'marker': '확인표시', 'EchoFixture': '되돌림시험서버', 'command': 'आदेश', 'out': 'मापन_लगत', 'expected': '예상결과', 'server_source': 'सर्भर_स्रोत', 'shell': 'शेल', 'upload': 'अपलोड_गर्नुहोस्_फाइलहरू', 'transcript': '대화기록', 'port': '접속번호', 'native': '자체실행파일', 'elf': '실행파일', 'server_udp_port': '서버전문접속번호', 'packed': '묶인자료', 'bridge': 'ब्रिज', 'selector': 'चयनकर्ता', 'end': 'समाप्त_गर्नुहोस्_अफसेट', 'e': '보조항목', 'ftp': 'फाइल_ट्रान्सफर_जडान', 'key': '누름값', 'bytecode': '바이트코드', 'peer': 'समान_मान', 'result': 'मापन', 'unchanged': '보존자료', 'line': 'रेखा', 'server_tcp_port': 'सर्भर_प्रवाह_पोर्ट', 'source': '원본자료', 'NetworkBridge': 'सञ्जाल_ब्रिज', 'jar': '자바꾸러미', 'receive': '수신하기', 'report': 'वैधानिकता_रिपोर्ट'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
