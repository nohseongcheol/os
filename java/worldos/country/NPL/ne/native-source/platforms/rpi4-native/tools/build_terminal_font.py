#!/usr/bin/env python3
"""기존 मार्ग 호환 प्रविष्टि_अंक. वास्तविक_लगत 구현: ../उपकरणहरू/बनाउनुहोस्_टर्मिनल_फन्ट.py"""
import importlib as 가져오기
import sys as सञ्चालनप्रणाली_मान
from pathlib import Path as मार्ग
सञ्चालनप्रणाली_मान.path.insert(0, str(मार्ग(__file__).resolve().parents[1] / 'उपकरणहरू'))
if __name__ == '__main__':
    import runpy as अनुप्रयोग_कर्मचारी_अगुवा
    अनुप्रयोग_कर्मचारी_अगुवा.run_module('बनाउनुहोस्_टर्मिनल_फन्ट', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('बनाउनुहोस्_टर्मिनल_फन्ट')
    대응 = {'data': 'लगत', 'img': 'चित्रकारी_मान', 'bits': '비트들', 'x': 'x_समन्वय', 'draw': '화면그리기', 'licences': '이용허락목록', 'paths': 'बाटो_सूची', 'y': '세로좌표', 'main': 'चलाउनुहोस्', 'src': '원본주소', 'fonts': 'फन्ट_सूची', 'ROOT': 'परियोजना_रूट', 'p': 'लगत_राख्नुहोस्', 'cp': 'वर्ण_एनकोडिङ', 'target': 'लक्ष्य'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
