#!/usr/bin/env python3
"""기존 मार्ग 호환 प्रविष्टि_अंक. वास्तविक_लगत 구현: ../उपकरणहरू/되돌림시험서버.py"""
import importlib as 가져오기
import sys as सञ्चालनप्रणाली_मान
from pathlib import Path as मार्ग
सञ्चालनप्रणाली_मान.path.insert(0, str(मार्ग(__file__).resolve().parents[1] / 'उपकरणहरू'))
if __name__ == '__main__':
    import runpy as अनुप्रयोग_कर्मचारी_अगुवा
    अनुप्रयोग_कर्मचारी_अगुवा.run_module('되돌림시험서버', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('되돌림시험서버')
    대응 = {'data': 'लगत', 'e': '보조항목', 'connection': 'जडान_e05f319b', 'f': 'फाइल_प्रविष्टि', 'peer': 'समान_मान', 'self': '자신', 'udp': '전문제어', 't': 'टर्मिनल_प्रविष्टि', 'tcp': 'जडान_नियन्त्रण', 'EchoFixture': '되돌림시험서버', 'args': 'तर्क_विन्यास', 'chunk': '조각'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
