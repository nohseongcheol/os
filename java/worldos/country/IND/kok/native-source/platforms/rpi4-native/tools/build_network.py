#!/usr/bin/env python3
"""기존 पाथ 호환 प्रवेश_पॉयंट. प्रत्यक्ष_डेटा 구현: ../साधनां/दाळचे_नॅटवर्क.py"""
import importlib as TAKE_मोल
import sys as ऑपरेटिंग_प्रणाली_मोल
from pathlib import Path as पाथ
ऑपरेटिंग_प्रणाली_मोल.path.insert(0, str(पाथ(__file__).resolve().parents[1] / 'साधनां'))
if __name__ == '__main__':
    import runpy as एप्लिकेशन_ऍप्लिकेशन_ड्रॉवर
    एप्लिकेशन_ऍप्लिकेशन_ड्रॉवर.run_module('दाळचे_नॅटवर्क', run_name='__main__', alter_sys=True)
else:
    구현 = TAKE_मोल.import_module('दाळचे_नॅटवर्क')
    대응 = {'obj': 'नियुक्त_स्थानाची_फायल', 'objects': 'नियुक्त_स्थान_फायली', 'library': 'लायब्ररी', 'output': '출력결과', 'port': '접속번호', 'root': 'रूट_नामो', 'files': 'फायल_सुची', 'source': '원본자료', 'run': 'पाळो_दिवचो_आदेश', 'flags': '설정비트', 'path': 'पाथ', 'build_network': 'निर्माण_करचें_नॅटवर्क', 'cc': '시언어번역기', 'ar': 'संग्रह_साधन'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
