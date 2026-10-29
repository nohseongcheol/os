#!/usr/bin/env python3
"""기존 पाथ 호환 प्रवेश_पॉयंट. प्रत्यक्ष_डेटा 구현: ../साधनां/화면요소시험.py"""
import importlib as TAKE_मोल
import sys as ऑपरेटिंग_प्रणाली_मोल
from pathlib import Path as पाथ
ऑपरेटिंग_प्रणाली_मोल.path.insert(0, str(पाथ(__file__).resolve().parents[1] / 'साधनां'))
if __name__ == '__main__':
    import runpy as एप्लिकेशन_ऍप्लिकेशन_ड्रॉवर
    एप्लिकेशन_ऍप्लिकेशन_ड्रॉवर.run_module('화면요소시험', run_name='__main__', alter_sys=True)
else:
    구현 = TAKE_मोल.import_module('화면요소시험')
    대응 = {'wait': '기다리기', 'x': 'x_coordinate', 's': 'स्ट्रिंग_डेटा', 'i': '순번', 'sel': 'वेंचक_a916db4e', 'seconds': '초단위', 'log': 'LOG_नोंद', 'data': 'डेटा', 'at': '현재위치', 'send': 'धाडचें', 'main': 'चलोवप', 'req': '요청값', 'hot': 'आडवाट_मोल', 'pump': 'हँडल_प्रसंग', 'ROOT': 'प्रॉजॅक्ट_रूट', 'marker': '확인표시', 'b': 'SECOND_मोल', 'command': 'आदेश', 'shell': 'शॅल', 'f': 'फायल_प्रवेश', 'click': 'क्लिक_करचें_बटन', 'k': '셋째순번', 'c': 'वर्ण_कोड', 'r': '반환값', 'p': 'डेटा_स्थिती', 'command_mode': 'आदेश_मोड', 'end': 'सोपोवचें_ऑफसॅट', 'classes': 'वर्ग_पाथ', 'key': '누름값', 'y': '세로좌표', 'result': 'मेजप', 'report': 'वैधताय_अहवाल', 'dest': 'नियुक्त_स्थान_मोल_स्थिती', 'work': '작업경로', 'qmp': '모의제어접속'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
