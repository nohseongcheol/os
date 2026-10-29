#!/usr/bin/env python3
"""기존 मार्ग 호환 प्रविष्टि_अंक. वास्तविक_लगत 구현: ../उपकरणहरू/원격한글시험.py"""
import importlib as 가져오기
import sys as सञ्चालनप्रणाली_मान
from pathlib import Path as मार्ग
सञ्चालनप्रणाली_मान.path.insert(0, str(मार्ग(__file__).resolve().parents[1] / 'उपकरणहरू'))
if __name__ == '__main__':
    import runpy as अनुप्रयोग_कर्मचारी_अगुवा
    अनुप्रयोग_कर्मचारी_अगुवा.run_module('원격한글시험', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('원격한글시험')
    대응 = {'wait': '기다리기', 'typing': '글자입력', 'start': 'चलाउनुहोस्', 'profile': 'प्रोफाइल', 'focused': 'केन्द्रित', 'serial': '직렬입출력', 'keys': '누름열', 'server': 'सर्भर_मान', 'log': 'लग_रेकर्ड', 'args': 'तर्क_विन्यास', 'deadline': '마감시각', 'data': 'लगत', 'candidate': '후보', 'logs': '기록들', 'kw': '이름붙인인수', 'number': '수치', 'main': 'चलाउनुहोस्', 'ready': '준비완료', 'found': 'खोज_मापन', 'guest': 'अतिथि', 'ROOT': 'परियोजना_रूट', 'marker': '확인표시', 'text': 'पाठ', 'out': 'मापन_लगत', 'env': '환경', 'f': 'फाइल_प्रविष्टि', 'port': '접속번호', 'offset': 'अफसेट_मान', 'version': '판번호', 'p': 'लगत_राख्नुहोस्', 'selector': 'चयनकर्ता', 'xvfb': 'अवास्तविक_प्रदर्शन', 'display': 'प्रदर्शन', 'n': '개수', 'key': '누름값', 'processes': '실행과정들', 'rootfs': '뿌리파일계층', 'xdo': '가상입력도구', 'name': 'नाम', 'window': 'सन्झ्याल', 'report': 'वैधानिकता_रिपोर्ट', 'work': '작업경로'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
