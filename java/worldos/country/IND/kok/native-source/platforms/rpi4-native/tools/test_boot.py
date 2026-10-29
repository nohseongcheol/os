#!/usr/bin/env python3
"""기존 पाथ 호환 प्रवेश_पॉयंट. प्रत्यक्ष_डेटा 구현: ../साधनां/부팅시험.py"""
import importlib as TAKE_मोल
import sys as ऑपरेटिंग_प्रणाली_मोल
from pathlib import Path as पाथ
ऑपरेटिंग_प्रणाली_मोल.path.insert(0, str(पाथ(__file__).resolve().parents[1] / 'साधनां'))
if __name__ == '__main__':
    import runpy as एप्लिकेशन_ऍप्लिकेशन_ड्रॉवर
    एप्लिकेशन_ऍप्लिकेशन_ड्रॉवर.run_module('부팅시험', run_name='__main__', alter_sys=True)
else:
    구현 = TAKE_मोल.import_module('부팅시험')
    대응 = {'timeout': '시간제한', 'response': '응답자료', 'msg': 'नॅटवर्क_संदेश', 'exact': 'EXACT_मोल', 'markers': '확인표시들', 'i': '순번', 'match': '일치', 'execute': 'पाळो_दिवचो_कार्य', 'cancel': 'रद्द_करचें_क्रिया', 'cmd_byte': 'आदेश_बायट', 'reply': 'जाप_दिवप', 'points': '지점들', 'server': 'सर्वर_मोल', 'data': 'डेटा', 'prompt': 'तत्पर', 'enter': 'प्रवेश_करचो', 'imported': '들여온파일', 'send': 'धाडचें', 'main': 'चलोवप', 'ROOT': 'प्रॉजॅक्ट_रूट', 'text': 'SMS', 'first_gui': '첫화면', 'pixel': 'पिक्सॅल', 'java_class': '자바클래스', 'upload': 'अपलोड_करचें_फायली', 'pixels_file': 'पिक्सॅल_फायल', 'pixels_data': 'पिक्सॅल_डेटा', 'edit': 'संपादन_करचें_मोल', 'receive_until': '표시까지받기', 'selector': 'वेंचक', 'size': 'आवाठ', 'qmp_path': '모의제어경로', 'key': '누름값', 'second_gui': 'SECOND_GUI', 'y': '세로좌표', 'result': 'मेजप', 'samples': '예제들', 'client': 'क्लायंट', 'line': 'रेग', 'report': 'वैधताय_अहवाल', 'work': '작업경로', 'x': 'x_coordinate', 'python_checks': '파이썬검사', 'download': 'डावनलोड', 'greeting': '인사', 'dims': '치수', 'chunk': '조각', 'deadline': '마감시각', 'proc': 'प्रक्रिया', 'content': 'अनुक्रमणिका_मोल', 'block': 'डेटा_आडावचें', 'marker': '확인표시', 'command': 'आदेश', 'expected': '예상결과', 'shell': 'शॅल', 'drawing': 'रेखाटन_पाथ', 'f': 'फायल_प्रवेश', 'transcript': '대화기록', 'offset': 'ऑफसॅट_मोल', 'path': 'पाथ', 'screenshot': 'स्क्रिन_क्लिपींग', 'arguments': '전달인수', 'pixels': '화소들', 'viewer': '화면접속자', 'output': '출력결과', 'stream': 'Stream_मोल', 'cmd': '명령인수', 'name': 'नांव', 'qmp': '모의제어접속'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
