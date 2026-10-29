#!/usr/bin/env python3
"""기존 पाथ 호환 प्रवेश_पॉयंट. प्रत्यक्ष_डेटा 구현: ../साधनां/바탕화면시험.py"""
import importlib as TAKE_मोल
import sys as ऑपरेटिंग_प्रणाली_मोल
from pathlib import Path as पाथ
ऑपरेटिंग_प्रणाली_मोल.path.insert(0, str(पाथ(__file__).resolve().parents[1] / 'साधनां'))
if __name__ == '__main__':
    import runpy as एप्लिकेशन_ऍप्लिकेशन_ड्रॉवर
    एप्लिकेशन_ऍप्लिकेशन_ड्रॉवर.run_module('바탕화면시험', run_name='__main__', alter_sys=True)
else:
    구현 = TAKE_मोल.import_module('바탕화면시험')
    대응 = {'x': 'x_coordinate', 'typing': '글자입력', 'message': '알림문', 'start': 'चलोवप', 'down': '누르는중', 'exact': 'EXACT_मोल', 'i': '순번', 'press': '글쇠누르기', 'rectangles': '사각형들', 'sym': 'चिन्न', 'j': '안쪽순번', 'deadline': '마감시각', 'proc': 'प्रक्रिया', 'data': 'डेटा', 'main': 'चलोवप', 'w': '너비값', 'init': '초기값', 'block': 'डेटा_आडावचें', 'ROOT': 'प्रॉजॅक्ट_रूट', 'text': 'SMS', 'marker': '확인표시', 'report': 'वैधताय_अहवाल', 'until': '까지', 'clipboard': 'क्लिप_बोर्ड_मोल', 'dst': 'नियुक्त_स्थान_नामो', 'seen': '본항목들', 'poll': '준비살피미', 'transcript': '대화기록', 'port': '접속번호', 'offset': 'ऑफसॅट_मोल', 'h': '높이값', 'src': '원본주소', 'event': 'प्रसंग', 'encoding': 'वर्ण_संच', 'size': 'आवाठ', 'key': '누름값', 'pixels': '화소들', 'y': '세로좌표', 'output': '출력결과', 'symbol': 'चिन्न_मोल', 'client': 'क्लायंट', 'char': 'वर्ण_डेटा', 'rgb': '빛삼원색'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
