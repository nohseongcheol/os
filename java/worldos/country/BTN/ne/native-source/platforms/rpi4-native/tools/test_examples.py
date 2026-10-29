#!/usr/bin/env python3
"""기존 मार्ग 호환 प्रविष्टि_अंक. वास्तविक_लगत 구현: ../उपकरणहरू/예제시험.py"""
import importlib as 가져오기
import sys as सञ्चालनप्रणाली_मान
from pathlib import Path as मार्ग
सञ्चालनप्रणाली_मान.path.insert(0, str(मार्ग(__file__).resolve().parents[1] / 'उपकरणहरू'))
if __name__ == '__main__':
    import runpy as अनुप्रयोग_कर्मचारी_अगुवा
    अनुप्रयोग_कर्मचारी_अगुवा.run_module('예제시험', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('예제시험')
    대응 = {'count': '항목수', 'exact': '정확한값', 'expected_file': '예상파일', 'ftp_port': '파일전송접속번호', 'data': 'लगत', 'graphics_command': 'ग्राफिक्स_आदेश', 'main': 'चलाउनुहोस्', 'row': 'रेकर्ड_राख्नुहोस्', 'init': '초기값', 'target': 'लक्ष्य', 'ROOT': 'परियोजना_रूट', 'text': 'पाठ', 'binary': 'बाइनेरी', 'out': 'मापन_लगत', 'entry': 'प्रविष्टि_अंक', 'got': '받은수', 'port': '접속번호', 'graphics_start': 'सुरु_चित्रकारी', 'col': 'स्तम्भ_राख्नुहोस्', 'begin': 'सुरु_अफसेट', 'kind': 'कोटि_मान', 'selector': 'चयनकर्ता', 'n': '개수', 'key': '누름값', 'y': '세로좌표', 'client': 'ग्राहक', 'line': 'रेखा', 'report': 'वैधानिकता_रिपोर्ट', 'language': 'भाषा', 'x': 'x_समन्वय', 'start': 'चलाउनुहोस्', 'rgb': '빛삼원색', 'down': '누르는중', 'listing': 'पठाउनुहोस्_सूची', 'payload': 'पेलोड_लगत', 'proc': 'प्रक्रिया', 'w': '너비값', 'temporary': '임시자원', 'echo': '되돌림서버항목', 'label': 'नाम_तालिका', 'content': 'सामग्री_मान', 'argument': '전달값', 'EchoServers': '되돌림서버', 'marker': '확인표시', 'expected': '예상결과', 'test_language': 'test_언어', 'filename': 'फाइल_प्रविष्टि_नाम', 'shell': 'शेल', 'color': '색상', 'transcript': '대화기록', 'offset': 'अफसेट_मान', 'h': '높이값', 'run': 'कार्यान्वयन_गर्नुहोस्_आदेश', 'c': 'वर्ण_सङ्केत', 'path': 'मार्ग', 'encoding': 'वर्णसेट', 'end': 'समाप्त_गर्नुहोस्_अफसेट', 'ftp': 'फाइल_ट्रान्सफर_जडान', 'pixels': '화소들', 'symbol': 'चिन्ह_मान', 'source': '원본자료', 'name': 'नाम', 'receive': '수신하기', 'manifest': '꾸러미명세'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
