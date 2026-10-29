#!/usr/bin/env python3
"""기존 पथ 호환 प्रवेश_बिदुं. वास्तविक_डेटा 구현: ../उपकरण/창시험.py"""
import importlib as 가져오기
import sys as ऑपरेटिंग_सिस्टम_मान
from pathlib import Path as पथ
ऑपरेटिंग_सिस्टम_मान.path.insert(0, str(पथ(__file__).resolve().parents[1] / 'उपकरण'))
if __name__ == '__main__':
    import runpy as ऐप_लॉन्चर
    ऐप_लॉन्चर.run_module('창시험', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('창시험')
    대응 = {'wait': '기다리기', 'x': 'x_निर्देशांक', 's': 'स्ट्रिंग_डेटा', 'xy': 'समन्वय_जोड़ी', 'sel': 'सिलेक्टर_a916db4e', 'seconds': '초단위', 'log': 'लॉग_रिकॉर्ड', 'at': 'अद्यतित_पद', 'send': 'भेजें', 'main': 'चलाएँ', 'req': 'अनुरोध_मान', 'hot': 'हॉट_की_मान', 'pump': 'हैंडल_घटना', 'ROOT': 'प्रोजेक्ट_करें_मूल', 'marker': 'मार्कर', 'b': '둘째값', 'command': 'आदेश', 'shell': 'शेल', 'f': 'फ़ाइल_एन्ट्री', 'color': '색상', 'click': 'क्लिक_करना_बटन', 'k': '셋째순번', 'c': 'वर्ण_कोड', 'r': '반환값', 'p': 'डेटा_पद', 'done': 'पूर्ण_राशि', 'end': 'समाप्त_करें_ऑफ़सेट', 'command_mode': 'आदेश_मोड', 'key': '누름값', 'y': '세로좌표', 'pixels': '화소들', 'result': 'परिणाम', 'report': 'प्रमाणीकरण_रिपोर्ट', 'dest': 'गंतव्य_मान_पद', 'work': '작업경로', 'qmp': '모의제어접속'}
    for 이전, अद्यतित_आइटम in 대응.items():
        if hasattr(구현, अद्यतित_आइटम): globals()[이전] = getattr(구현, अद्यतित_आइटम)
