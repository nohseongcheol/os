#!/usr/bin/env python3
"""기존 मार्ग 호환 प्रविष्टि_अंक. वास्तविक_लगत 구현: ../उपकरणहरू/바탕화면시험.py"""
import importlib as 가져오기
import sys as सञ्चालनप्रणाली_मान
from pathlib import Path as मार्ग
सञ्चालनप्रणाली_मान.path.insert(0, str(मार्ग(__file__).resolve().parents[1] / 'उपकरणहरू'))
if __name__ == '__main__':
    import runpy as अनुप्रयोग_कर्मचारी_अगुवा
    अनुप्रयोग_कर्मचारी_अगुवा.run_module('바탕화면시험', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('바탕화면시험')
    대응 = {'x': 'x_समन्वय', 'typing': '글자입력', 'message': '알림문', 'start': 'चलाउनुहोस्', 'down': '누르는중', 'exact': '정확한값', 'i': '순번', 'press': '글쇠누르기', 'rectangles': '사각형들', 'sym': 'चिन्ह', 'j': '안쪽순번', 'deadline': '마감시각', 'proc': 'प्रक्रिया', 'data': 'लगत', 'main': 'चलाउनुहोस्', 'w': '너비값', 'init': '초기값', 'block': 'लगत_छेक्नुहोस्', 'ROOT': 'परियोजना_रूट', 'text': 'पाठ', 'marker': '확인표시', 'report': 'वैधानिकता_रिपोर्ट', 'until': '까지', 'clipboard': 'क्लिपबोर्ड_मान', 'dst': 'गन्तव्य_ठेगाना', 'seen': '본항목들', 'poll': '준비살피미', 'transcript': '대화기록', 'port': '접속번호', 'offset': 'अफसेट_मान', 'h': '높이값', 'src': '원본주소', 'event': 'घटना', 'encoding': 'वर्णसेट', 'size': 'आकार', 'key': '누름값', 'pixels': '화소들', 'y': '세로좌표', 'output': '출력결과', 'symbol': 'चिन्ह_मान', 'client': 'ग्राहक', 'char': 'वर्ण_लगत', 'rgb': '빛삼원색'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
