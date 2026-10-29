#!/usr/bin/env python3
"""기존 मार्ग 호환 प्रविष्टि_अंक. वास्तविक_लगत 구현: ../उपकरणहरू/셸시험.py"""
import importlib as 가져오기
import sys as सञ्चालनप्रणाली_मान
from pathlib import Path as मार्ग
सञ्चालनप्रणाली_मान.path.insert(0, str(मार्ग(__file__).resolve().parents[1] / 'उपकरणहरू'))
if __name__ == '__main__':
    import runpy as अनुप्रयोग_कर्मचारी_अगुवा
    अनुप्रयोग_कर्मचारी_अगुवा.run_module('셸시험', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('셸시험')
    대응 = {'timeout': '시간제한', 'x': 'x_समन्वय', 'msg': 'सञ्जाल_सन्देश', 'i': '순번', 'reply': 'जवाफ_दिनुहोस्', 'call': '호출', 'args': 'तर्क_विन्यास', 'chunk': '조각', 'data': 'लगत', 'proc': 'प्रक्रिया', 'long_text': '긴글', 'restored': '복원자료', 'send': 'पठाउनुहोस्', 'file': 'फाइल', 'main': 'चलाउनुहोस्', 'found': 'खोज_मापन', 'ROOT': 'परियोजना_रूट', 'text': 'पाठ', 'marker': '확인표시', 'command': 'आदेश', 'expected': '예상결과', 'pixel': 'पेल', 'shell': 'शेल', 'poll': '준비살피미', 'transcript': '대화기록', 'end': 'समाप्त_गर्नुहोस्_अफसेट', 'image': 'छवि', 'key': '누름값', 'y': '세로좌표', 'output': '출력결과', 'result': 'मापन', 'client': 'ग्राहक', 'line': 'रेखा', 'stream': 'प्रवाह_मान', 'name': 'नाम', 'value': 'मान', 'receive': '수신하기', 'report': 'वैधानिकता_रिपोर्ट', 'work': '작업경로', 'qmp': '모의제어접속'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
