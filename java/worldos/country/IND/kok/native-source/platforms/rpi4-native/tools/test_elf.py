#!/usr/bin/env python3
"""기존 पाथ 호환 प्रवेश_पॉयंट. प्रत्यक्ष_डेटा 구현: ../साधनां/실행파일시험.py"""
import importlib as TAKE_मोल
import sys as ऑपरेटिंग_प्रणाली_मोल
from pathlib import Path as पाथ
ऑपरेटिंग_प्रणाली_मोल.path.insert(0, str(पाथ(__file__).resolve().parents[1] / 'साधनां'))
if __name__ == '__main__':
    import runpy as एप्लिकेशन_ऍप्लिकेशन_ड्रॉवर
    एप्लिकेशन_ऍप्लिकेशन_ड्रॉवर.run_module('실행파일시험', run_name='__main__', alter_sys=True)
else:
    구현 = TAKE_मोल.import_module('실행파일시험')
    대응 = {'out': 'मेजप_डेटा', 'expected': '예상결과', 'phoff': 'एप्लिकेशन_माथाळो_ऑफसॅट', 'offset': 'ऑफसॅट_मोल', 'invalid': 'अवैध_डेटा', 'path': 'पाथ', 'executable': '실행가능파일', 'rejected': '거부결과', 'linux_example': '리눅스예제', 'original': '원본', 'result': 'मेजप', 'format_': 'स्वरूप_b87fd068', 'main': 'चलोवप', 'content': 'अनुक्रमणिका_मोल', 'source': '원본자료', 'name': 'नांव', 'reference': '비교기준', 'ROOT': 'प्रॉजॅक्ट_रूट', 'value': 'मोल', 'report': 'वैधताय_अहवाल'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
