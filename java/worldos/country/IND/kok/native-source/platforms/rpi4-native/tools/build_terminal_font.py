#!/usr/bin/env python3
"""기존 पाथ 호환 प्रवेश_पॉयंट. प्रत्यक्ष_डेटा 구현: ../साधनां/दाळचे_टर्मिनल_फाँट.py"""
import importlib as TAKE_मोल
import sys as ऑपरेटिंग_प्रणाली_मोल
from pathlib import Path as पाथ
ऑपरेटिंग_प्रणाली_मोल.path.insert(0, str(पाथ(__file__).resolve().parents[1] / 'साधनां'))
if __name__ == '__main__':
    import runpy as एप्लिकेशन_ऍप्लिकेशन_ड्रॉवर
    एप्लिकेशन_ऍप्लिकेशन_ड्रॉवर.run_module('दाळचे_टर्मिनल_फाँट', run_name='__main__', alter_sys=True)
else:
    구현 = TAKE_मोल.import_module('दाळचे_टर्मिनल_फाँट')
    대응 = {'data': 'डेटा', 'img': 'रेखाटन_मोल', 'bits': '비트들', 'x': 'x_coordinate', 'draw': '화면그리기', 'licences': '이용허락목록', 'paths': 'पाथ_सुची', 'y': '세로좌표', 'main': 'चलोवप', 'src': '원본주소', 'fonts': 'फाँट_सुची', 'ROOT': 'प्रॉजॅक्ट_रूट', 'p': 'डेटा_स्थिती', 'cp': 'वर्ण_एनकोडिंग', 'target': 'लक्ष्य'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
