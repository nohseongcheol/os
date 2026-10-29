#!/usr/bin/env python3
"""기존 पाथ 호환 प्रवेश_पॉयंट. प्रत्यक्ष_डेटा 구현: ../साधनां/예제시험.py"""
import importlib as TAKE_मोल
import sys as ऑपरेटिंग_प्रणाली_मोल
from pathlib import Path as पाथ
ऑपरेटिंग_प्रणाली_मोल.path.insert(0, str(पाथ(__file__).resolve().parents[1] / 'साधनां'))
if __name__ == '__main__':
    import runpy as एप्लिकेशन_ऍप्लिकेशन_ड्रॉवर
    एप्लिकेशन_ऍप्लिकेशन_ड्रॉवर.run_module('예제시험', run_name='__main__', alter_sys=True)
else:
    구현 = TAKE_मोल.import_module('예제시험')
    대응 = {'count': 'प्रवेश_COUNT', 'exact': 'EXACT_मोल', 'expected_file': '예상파일', 'ftp_port': '파일전송접속번호', 'data': 'डेटा', 'graphics_command': 'ग्राफिक्स_आदेश', 'main': 'चलोवप', 'row': 'ROW_स्थिती', 'init': '초기값', 'target': 'लक्ष्य', 'ROOT': 'प्रॉजॅक्ट_रूट', 'text': 'SMS', 'binary': 'बायनरी', 'out': 'मेजप_डेटा', 'entry': 'प्रवेश_पॉयंट', 'got': 'RECEIVED_COUNT', 'port': '접속번호', 'graphics_start': 'Start_रेखाटन', 'col': 'स्तंभ_स्थिती', 'begin': 'Start_ऑफसॅट', 'kind': 'वर्ग_मोल', 'selector': 'वेंचक', 'n': 'आयटम_COUNT', 'key': '누름값', 'y': '세로좌표', 'client': 'क्लायंट', 'line': 'रेग', 'report': 'वैधताय_अहवाल', 'language': 'भास', 'x': 'x_coordinate', 'start': 'चलोवप', 'rgb': '빛삼원색', 'down': '누르는중', 'listing': 'धाडचें_सुची', 'payload': 'पेलोड_डेटा', 'proc': 'प्रक्रिया', 'w': '너비값', 'temporary': '임시자원', 'echo': '되돌림서버항목', 'label': 'नांव_तकटो', 'content': 'अनुक्रमणिका_मोल', 'argument': '전달값', 'EchoServers': '되돌림서버', 'marker': '확인표시', 'expected': '예상결과', 'test_language': 'test_언어', 'filename': 'फायल_प्रवेश_नांव', 'shell': 'शॅल', 'color': '색상', 'transcript': '대화기록', 'offset': 'ऑफसॅट_मोल', 'h': '높이값', 'run': 'पाळो_दिवचो_आदेश', 'c': 'वर्ण_कोड', 'path': 'पाथ', 'encoding': 'वर्ण_संच', 'end': 'सोपोवचें_ऑफसॅट', 'ftp': 'फायल_ट्रान्सफर_कनॅक्शन', 'pixels': '화소들', 'symbol': 'चिन्न_मोल', 'source': '원본자료', 'name': 'नांव', 'receive': '수신하기', 'manifest': '꾸러미명세'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
