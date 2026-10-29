#!/usr/bin/env python3
"""기존 मार्ग 호환 प्रविष्टि_अंक. वास्तविक_लगत 구현: ../उपकरणहरू/부팅시험.py"""
import importlib as 가져오기
import sys as सञ्चालनप्रणाली_मान
from pathlib import Path as मार्ग
सञ्चालनप्रणाली_मान.path.insert(0, str(मार्ग(__file__).resolve().parents[1] / 'उपकरणहरू'))
if __name__ == '__main__':
    import runpy as अनुप्रयोग_कर्मचारी_अगुवा
    अनुप्रयोग_कर्मचारी_अगुवा.run_module('부팅시험', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('부팅시험')
    대응 = {'timeout': '시간제한', 'response': '응답자료', 'msg': 'सञ्जाल_सन्देश', 'exact': '정확한값', 'markers': '확인표시들', 'i': '순번', 'match': '일치', 'execute': 'कार्यान्वयन_गर्नुहोस्', 'cancel': 'रद्द_गर्नुहोस्_सञ्चालन', 'cmd_byte': 'आदेश_बाइट', 'reply': 'जवाफ_दिनुहोस्', 'points': '지점들', 'server': 'सर्भर_मान', 'data': 'लगत', 'prompt': 'प्रम्प्ट', 'enter': 'प्रविष्टि_गराउनुहोस्', 'imported': '들여온파일', 'send': 'पठाउनुहोस्', 'main': 'चलाउनुहोस्', 'ROOT': 'परियोजना_रूट', 'text': 'पाठ', 'first_gui': '첫화면', 'pixel': 'पेल', 'java_class': '자바클래스', 'upload': 'अपलोड_गर्नुहोस्_फाइलहरू', 'pixels_file': 'पेल_फाइल', 'pixels_data': 'पेल_लगत', 'edit': 'सम्पादन_गर्नुहोस्_मान', 'receive_until': '표시까지받기', 'selector': 'चयनकर्ता', 'size': 'आकार', 'qmp_path': '모의제어경로', 'key': '누름값', 'second_gui': '둘째화면', 'y': '세로좌표', 'result': 'मापन', 'samples': '예제들', 'client': 'ग्राहक', 'line': 'रेखा', 'report': 'वैधानिकता_रिपोर्ट', 'work': '작업경로', 'x': 'x_समन्वय', 'python_checks': '파이썬검사', 'download': 'डाउनलोड', 'greeting': '인사', 'dims': '치수', 'chunk': '조각', 'deadline': '마감시각', 'proc': 'प्रक्रिया', 'content': 'सामग्री_मान', 'block': 'लगत_छेक्नुहोस्', 'marker': '확인표시', 'command': 'आदेश', 'expected': '예상결과', 'shell': 'शेल', 'drawing': 'चित्रकारी_बाटो', 'f': 'फाइल_प्रविष्टि', 'transcript': '대화기록', 'offset': 'अफसेट_मान', 'path': 'मार्ग', 'screenshot': 'स्क्रिन_क्लिपिङ्', 'arguments': '전달인수', 'pixels': '화소들', 'viewer': '화면접속자', 'output': '출력결과', 'stream': 'प्रवाह_मान', 'cmd': '명령인수', 'name': 'नाम', 'qmp': '모의제어접속'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
