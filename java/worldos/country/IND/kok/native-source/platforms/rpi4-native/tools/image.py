#!/usr/bin/env python3
"""기존 पाथ 호환 प्रवेश_पॉयंट. प्रत्यक्ष_डेटा 구현: ../साधनां/निर्माण_करचें_IMAGE.py"""
import importlib as TAKE_मोल
import sys as ऑपरेटिंग_प्रणाली_मोल
from pathlib import Path as पाथ
ऑपरेटिंग_प्रणाली_मोल.path.insert(0, str(पाथ(__file__).resolve().parents[1] / 'साधनां'))
if __name__ == '__main__':
    import runpy as एप्लिकेशन_ऍप्लिकेशन_ड्रॉवर
    एप्लिकेशन_ऍप्लिकेशन_ड्रॉवर.run_module('निर्माण_करचें_IMAGE', run_name='__main__', alter_sys=True)
else:
    구현 = TAKE_मोल.import_module('निर्माण_करचें_IMAGE')
    대응 = {'total': '총량', 'start': 'चलोवप', 'firmware': '기초제어프로그램', 'files': 'फायल_सुची', 'archive_base': 'संग्रह_BASE', 'partition': 'विभागणी_फायल', 'archive': 'संग्रह', 'main': 'चलोवप', 'block': 'डेटा_आडावचें', 'ROOT': 'प्रॉजॅक्ट_रूट', 'boot': '부팅경로', 'stage': 'पांवडो_मोल', 'out': 'मेजप_डेटा', 'expected': '예상결과', 'f': 'फायल_प्रवेश', 'src': '원본주소', 'path': 'पाथ', 'p': 'डेटा_स्थिती', 'extracted': '추출자료', 'member': 'वांगडी', 'mbr': '주부트기록', 'image': 'IMAGE', 'sector_count': '섹터개수', 'dist': '배포경로', 'sha': '해시계산', 'license_': 'परवानो_दिवचो', 'source': '원본자료', 'name': 'नांव', 'value': 'मोल', 'manifest': '꾸러미명세', 'dest': 'नियुक्त_स्थान_मोल_स्थिती', 'work': '작업경로'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
