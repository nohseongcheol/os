#!/usr/bin/env python3
"""기존 मार्ग 호환 प्रविष्टि_अंक. वास्तविक_लगत 구현: ../उपकरणहरू/실행파일시험.py"""
import importlib as 가져오기
import sys as सञ्चालनप्रणाली_मान
from pathlib import Path as मार्ग
सञ्चालनप्रणाली_मान.path.insert(0, str(मार्ग(__file__).resolve().parents[1] / 'उपकरणहरू'))
if __name__ == '__main__':
    import runpy as अनुप्रयोग_कर्मचारी_अगुवा
    अनुप्रयोग_कर्मचारी_अगुवा.run_module('실행파일시험', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('실행파일시험')
    대응 = {'out': 'मापन_लगत', 'expected': '예상결과', 'phoff': 'अनुप्रयोग_हेडर_अफसेट', 'offset': 'अफसेट_मान', 'invalid': 'अवैधानिक_लगत', 'path': 'मार्ग', 'executable': '실행가능파일', 'rejected': '거부결과', 'linux_example': '리눅스예제', 'original': '원본', 'result': 'मापन', 'format_': 'ढाँचा_b87fd068', 'main': 'चलाउनुहोस्', 'content': 'सामग्री_मान', 'source': '원본자료', 'name': 'नाम', 'reference': 'तुलना_आधाररेखा', 'ROOT': 'परियोजना_रूट', 'value': 'मान', 'report': 'वैधानिकता_रिपोर्ट'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
