#!/usr/bin/env python3
"""기존 पाथ 호환 प्रवेश_पॉयंट. प्रत्यक्ष_डेटा 구현: ../साधनां/पाळो_दिवचो_आदेश.py"""
import importlib as TAKE_मोल
import sys as ऑपरेटिंग_प्रणाली_मोल
from pathlib import Path as पाथ
ऑपरेटिंग_प्रणाली_मोल.path.insert(0, str(पाथ(__file__).resolve().parents[1] / 'साधनां'))
if __name__ == '__main__':
    import runpy as एप्लिकेशन_ऍप्लिकेशन_ड्रॉवर
    एप्लिकेशन_ऍप्लिकेशन_ड्रॉवर.run_module('पाळो_दिवचो_आदेश', run_name='__main__', alter_sys=True)
else:
    구현 = TAKE_मोल.import_module('पाळो_दिवचो_आदेश')
    대응 = {'supported': '지원목록', 'parser': '인수해석기', 'qemu': '모의기계', 'run_desktop': 'चलोवप_डॅस्कटॉप', 'main': 'चलोवप', 'host': 'येजमान', 'status': 'स्थिती_मोल_e10195a1', 'NetworkBridge': 'नॅटवर्क_ब्रिज', 'ROOT': 'प्रॉजॅक्ट_रूट', 'bridge': 'ब्रिज', 'loader': '적재기', 'base': 'फाटभूंय_मोल', 'options': 'पर्याय', 'binary': 'बायनरी', 'args': 'युक्तीवाद_क्रम', 'command': 'आदेश'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
