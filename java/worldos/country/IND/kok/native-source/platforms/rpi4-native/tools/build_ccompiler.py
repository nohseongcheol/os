#!/usr/bin/env python3
"""기존 पाथ 호환 प्रवेश_पॉयंट. प्रत्यक्ष_डेटा 구현: ../साधनां/시언어번역기빌드.py"""
import importlib as TAKE_मोल
import sys as ऑपरेटिंग_प्रणाली_मोल
from pathlib import Path as पाथ
ऑपरेटिंग_प्रणाली_मोल.path.insert(0, str(पाथ(__file__).resolve().parents[1] / 'साधनां'))
if __name__ == '__main__':
    import runpy as एप्लिकेशन_ऍप्लिकेशन_ड्रॉवर
    एप्लिकेशन_ऍप्लिकेशन_ड्रॉवर.run_module('시언어번역기빌드', run_name='__main__', alter_sys=True)
else:
    구현 = TAKE_मोल.import_module('시언어번역기빌드')
    대응 = {'out': 'मेजप_डेटा', 'builtins': '내장연산', 'header': 'माथाळो_मोल', 'sdk': '개발꾸러미', 'build_ccompiler': '시언어번역기만들기', 'i': '순번', 'elf': '실행파일', 'run': 'पाळो_दिवचो_आदेश', 'flags': '설정비트', 'path': 'पाथ', 'p': 'डेटा_स्थिती', 'cc': '시언어번역기', 'obj': 'नियुक्त_स्थानाची_फायल', 'flag': 'मांडावळी_मोल', 'ld': '연결편집기', 'objects': 'नियुक्त_स्थान_फायली', 'repo': '저장소경로', 'v': '임시값', 'upstream': '외부원문', 'root': 'रूट_नामो', 'assets': '탑재자료', 'source': '원본자료', 'name': 'नांव', 'includes': '포함인수'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
