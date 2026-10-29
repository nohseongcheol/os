#!/usr/bin/env python3
"""기존 पाथ 호환 प्रवेश_पॉयंट. प्रत्यक्ष_डेटा 구현: ../साधनां/दाळचे_PYTHON.py"""
import importlib as TAKE_मोल
import sys as ऑपरेटिंग_प्रणाली_मोल
from pathlib import Path as पाथ
ऑपरेटिंग_प्रणाली_मोल.path.insert(0, str(पाथ(__file__).resolve().parents[1] / 'साधनां'))
if __name__ == '__main__':
    import runpy as एप्लिकेशन_ऍप्लिकेशन_ड्रॉवर
    एप्लिकेशन_ऍप्लिकेशन_ड्रॉवर.run_module('दाळचे_PYTHON', run_name='__main__', alter_sys=True)
else:
    구현 = TAKE_मोल.import_module('दाळचे_PYTHON')
    대응 = {'ld': '연결편집기', 'archive': 'संग्रह', 'SHA256': 'वैधताय_हॅश', 'build_python': 'निर्माण_करचें_PYTHON', 'root': 'रूट_नामो', 'source': '원본자료', 'name': 'नांव', 'path': 'पाथ', 'VERSION': '배포판', 'cc': '시언어번역기', 'tar': '타르꾸러미', 'newlib': '뉴리브포함경로', 'member': 'वांगडी'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
