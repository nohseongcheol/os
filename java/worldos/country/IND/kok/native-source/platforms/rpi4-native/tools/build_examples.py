#!/usr/bin/env python3
"""기존 पाथ 호환 प्रवेश_पॉयंट. प्रत्यक्ष_डेटा 구현: ../साधनां/예제빌드.py"""
import importlib as TAKE_मोल
import sys as ऑपरेटिंग_प्रणाली_मोल
from pathlib import Path as पाथ
ऑपरेटिंग_प्रणाली_मोल.path.insert(0, str(पाथ(__file__).resolve().parents[1] / 'साधनां'))
if __name__ == '__main__':
    import runpy as एप्लिकेशन_ऍप्लिकेशन_ड्रॉवर
    एप्लिकेशन_ऍप्लिकेशन_ड्रॉवर.run_module('예제빌드', run_name='__main__', alter_sys=True)
else:
    구현 = TAKE_मोल.import_module('예제빌드')
    대응 = {'out': 'मेजप_डेटा', 'build_examples': '예제만들기', 'files': 'फायल_सुची', 'java': '자바실행', 'run': 'पाळो_दिवचो_आदेश', 'path': 'पाथ', 'p': 'डेटा_स्थिती', 'readme': 'README', 'build_java_library': '자바라이브러리만들기', 'code': 'समजावणी_SEQUENCE', 'index': 'लूकअप_INDEX', 'classes': 'वर्ग_पाथ', 'repo': '저장소경로', 'root': 'रूट_नामो', 'content': 'अनुक्रमणिका_मोल', 'source': '원본자료', 'name': 'नांव', 'target': 'लक्ष्य', 'manifest': '꾸러미명세', 'language': 'भास'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
