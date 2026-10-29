#!/usr/bin/env python3
"""기존 पाथ 호환 प्रवेश_पॉयंट. प्रत्यक्ष_डेटा 구현: ../साधनां/원격한글시험.py"""
import importlib as TAKE_मोल
import sys as ऑपरेटिंग_प्रणाली_मोल
from pathlib import Path as पाथ
ऑपरेटिंग_प्रणाली_मोल.path.insert(0, str(पाथ(__file__).resolve().parents[1] / 'साधनां'))
if __name__ == '__main__':
    import runpy as एप्लिकेशन_ऍप्लिकेशन_ड्रॉवर
    एप्लिकेशन_ऍप्लिकेशन_ड्रॉवर.run_module('원격한글시험', run_name='__main__', alter_sys=True)
else:
    구현 = TAKE_मोल.import_module('원격한글시험')
    대응 = {'wait': '기다리기', 'typing': '글자입력', 'start': 'चलोवप', 'profile': 'प्रोफायल', 'focused': 'केंद्रीत', 'serial': '직렬입출력', 'keys': '누름열', 'server': 'सर्वर_मोल', 'log': 'LOG_नोंद', 'args': 'युक्तीवाद_क्रम', 'deadline': '마감시각', 'data': 'डेटा', 'candidate': '후보', 'logs': '기록들', 'kw': '이름붙인인수', 'number': '수치', 'main': 'चलोवप', 'ready': '준비완료', 'found': 'सोद_मेजप', 'guest': 'सोयरो', 'ROOT': 'प्रॉजॅक्ट_रूट', 'marker': '확인표시', 'text': 'SMS', 'out': 'मेजप_डेटा', 'env': '환경', 'f': 'फायल_प्रवेश', 'port': '접속번호', 'offset': 'ऑफसॅट_मोल', 'version': '판번호', 'p': 'डेटा_स्थिती', 'selector': 'वेंचक', 'xvfb': 'भ्रामक_प्रदर्शन', 'display': 'प्रदर्शन', 'n': 'आयटम_COUNT', 'key': '누름값', 'processes': '실행과정들', 'rootfs': '뿌리파일계층', 'xdo': '가상입력도구', 'name': 'नांव', 'window': 'विंडो', 'report': 'वैधताय_अहवाल', 'work': '작업경로'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
