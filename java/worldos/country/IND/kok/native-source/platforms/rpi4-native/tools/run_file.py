#!/usr/bin/env python3
"""기존 पाथ 호환 प्रवेश_पॉयंट. प्रत्यक्ष_डेटा 구현: ../साधनां/पाळो_दिवचो_फायल.py"""
import importlib as TAKE_मोल
import sys as ऑपरेटिंग_प्रणाली_मोल
from pathlib import Path as पाथ
ऑपरेटिंग_प्रणाली_मोल.path.insert(0, str(पाथ(__file__).resolve().parents[1] / 'साधनां'))
if __name__ == '__main__':
    import runpy as एप्लिकेशन_ऍप्लिकेशन_ड्रॉवर
    एप्लिकेशन_ऍप्लिकेशन_ड्रॉवर.run_module('पाळो_दिवचो_फायल', run_name='__main__', alter_sys=True)
else:
    구현 = TAKE_मोल.import_module('पाळो_दिवचो_फायल')
    대응 = {'timeout': '시간제한', 's': 'स्ट्रिंग_डेटा', 'i': '순번', 'match': '일치', 'files': 'फायल_सुची', 'program': 'एप्लिकेशन', 'executable': '실행가능파일', 'args': 'युक्तीवाद_क्रम', 'chunk': '조각', 'data': 'डेटा', 'proc': 'प्रक्रिया', 'send': 'धाडचें', 'main': 'चलोवप', 'marker': '확인표시', 'command': 'आदेश', 'include': '포함항목', 'dumped': '갈무리자료', 'run': 'पाळो_दिवचो_आदेश', 'p': 'डेटा_स्थिती', 'parser': '인수해석기', 'options': 'पर्याय', 'kind': 'वर्ग_मोल', 'selector': 'वेंचक', 'upload_data': 'अपलोड_करचें_डेटा', 'end': 'सोपोवचें_ऑफसॅट', 'n': 'आयटम_COUNT', 'd': 'नियुक्त_स्थान_डेटा', 'key': '누름값', 'output': '출력결과', 'line': 'रेग', 'name': 'नांव', 'upload_name': 'अपलोड_करचें_नांव', 'receive': '수신하기'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
