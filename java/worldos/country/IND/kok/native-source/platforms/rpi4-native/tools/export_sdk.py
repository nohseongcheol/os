#!/usr/bin/env python3
"""기존 पाथ 호환 प्रवेश_पॉयंट. प्रत्यक्ष_डेटा 구현: ../साधनां/개발꾸러미내보내기.py"""
import importlib as TAKE_मोल
import sys as ऑपरेटिंग_प्रणाली_मोल
from pathlib import Path as पाथ
ऑपरेटिंग_प्रणाली_मोल.path.insert(0, str(पाथ(__file__).resolve().parents[1] / 'साधनां'))
if __name__ == '__main__':
    import runpy as एप्लिकेशन_ऍप्लिकेशन_ड्रॉवर
    एप्लिकेशन_ऍप्लिकेशन_ड्रॉवर.run_module('개발꾸러미내보내기', run_name='__main__', alter_sys=True)
else:
    구현 = TAKE_मोल.import_module('개발꾸러미내보내기')
    대응 = {'out': 'मेजप_डेटा', 'obj': 'नियुक्त_स्थानाची_फायल', 'relative': '상대경로', 'compiler_archive': '번역기꾸러미', 'sdk': '개발꾸러미', 'dist': '배포경로', 'archive': 'संग्रह', 'main': 'चलोवप', 'posix': '포직스경로', 'files': 'फायल_सुची', 'source': '원본자료', 'name': 'नांव', 'target': 'लक्ष्य', 'ROOT': 'प्रॉजॅक्ट_रूट', 'destination': 'नियुक्त_स्थान_डेटा_नामो', 'manifest': '꾸러미명세', 'work': '작업경로'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
