#!/usr/bin/env python3
"""기존 मार्ग 호환 प्रविष्टि_अंक. वास्तविक_लगत 구현: ../उपकरणहरू/자바가상기계시험.py"""
import importlib as 가져오기
import sys as सञ्चालनप्रणाली_मान
from pathlib import Path as मार्ग
सञ्चालनप्रणाली_मान.path.insert(0, str(मार्ग(__file__).resolve().parents[1] / 'उपकरणहरू'))
if __name__ == '__main__':
    import runpy as अनुप्रयोग_कर्मचारी_अगुवा
    अनुप्रयोग_कर्मचारी_अगुवा.run_module('자바가상기계시험', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('자바가상기계시험')
    대응 = {'message': '알림문', 's': 'स्ट्रिङ_लगत', 'actual': 'वास्तविक_मापन', 'match': '일치', 'payload': 'पेलोड_लगत', 'cases': '시험사례', 'fixture': '시험자료', 'main': 'चलाउनुहोस्', 'ROOT': 'परियोजना_रूट', 'text': 'पाठ', 'valid': '유효함', 'includes': '포함인수', 'include': '포함항목', 'expected': '예상결과', 'sources': '원문목록', 'tmp': '임시경로', 'done': '완료량', 'classes': 'वर्ग_बाटो', 'output': '출력결과', 'result': 'मापन', 'cmd': '명령인수', 'name': 'नाम', 'jar': '자바꾸러미', 'report': 'वैधानिकता_रिपोर्ट', 'tests': '시험목록'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
