#!/usr/bin/env python3
"""기존 पाथ 호환 प्रवेश_पॉयंट. प्रत्यक्ष_डेटा 구현: ../साधनां/자바라이브러리빌드.py"""
import importlib as TAKE_मोल
import sys as ऑपरेटिंग_प्रणाली_मोल
from pathlib import Path as पाथ
ऑपरेटिंग_प्रणाली_मोल.path.insert(0, str(पाथ(__file__).resolve().parents[1] / 'साधनां'))
if __name__ == '__main__':
    import runpy as एप्लिकेशन_ऍप्लिकेशन_ड्रॉवर
    एप्लिकेशन_ऍप्लिकेशन_ड्रॉवर.run_module('자바라이브러리빌드', run_name='__main__', alter_sys=True)
else:
    구현 = TAKE_मोल.import_module('자바라이브러리빌드')
    대응 = {'header': 'माथाळो_मोल', 'sources': '원문목록', 'i': '순번', 'info': 'msinfo32_exe', 'payload': 'पेलोड_डेटा', 'src': '원본주소', 'run': 'पाळो_दिवचो_आदेश', 'build_java_library': '자바라이브러리만들기', 'relative': '상대경로', 'classes': 'वर्ग_पाथ', 'dist': '배포경로', 'archive': 'संग्रह', 'output': '출력결과', 'root': 'रूट_नामो', 'name': 'नांव', 'jar': '자바꾸러미', 'b': 'SECOND_मोल', 'entries': '항목들'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
