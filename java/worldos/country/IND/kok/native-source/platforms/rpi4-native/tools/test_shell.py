#!/usr/bin/env python3
"""기존 पाथ 호환 प्रवेश_पॉयंट. प्रत्यक्ष_डेटा 구현: ../साधनां/셸시험.py"""
import importlib as TAKE_मोल
import sys as ऑपरेटिंग_प्रणाली_मोल
from pathlib import Path as पाथ
ऑपरेटिंग_प्रणाली_मोल.path.insert(0, str(पाथ(__file__).resolve().parents[1] / 'साधनां'))
if __name__ == '__main__':
    import runpy as एप्लिकेशन_ऍप्लिकेशन_ड्रॉवर
    एप्लिकेशन_ऍप्लिकेशन_ड्रॉवर.run_module('셸시험', run_name='__main__', alter_sys=True)
else:
    구현 = TAKE_मोल.import_module('셸시험')
    대응 = {'timeout': '시간제한', 'x': 'x_coordinate', 'msg': 'नॅटवर्क_संदेश', 'i': '순번', 'reply': 'जाप_दिवप', 'call': '호출', 'args': 'युक्तीवाद_क्रम', 'chunk': '조각', 'data': 'डेटा', 'proc': 'प्रक्रिया', 'long_text': '긴글', 'restored': '복원자료', 'send': 'धाडचें', 'file': 'फायल', 'main': 'चलोवप', 'found': 'सोद_मेजप', 'ROOT': 'प्रॉजॅक्ट_रूट', 'text': 'SMS', 'marker': '확인표시', 'command': 'आदेश', 'expected': '예상결과', 'pixel': 'पिक्सॅल', 'shell': 'शॅल', 'poll': '준비살피미', 'transcript': '대화기록', 'end': 'सोपोवचें_ऑफसॅट', 'image': 'IMAGE', 'key': '누름값', 'y': '세로좌표', 'output': '출력결과', 'result': 'मेजप', 'client': 'क्लायंट', 'line': 'रेग', 'stream': 'Stream_मोल', 'name': 'नांव', 'value': 'मोल', 'receive': '수신하기', 'report': 'वैधताय_अहवाल', 'work': '작업경로', 'qmp': '모의제어접속'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
