#!/usr/bin/env python3
"""기존 मार्ग 호환 प्रविष्टि_अंक. वास्तविक_लगत 구현: ../उपकरणहरू/कार्यान्वयन_गर्नुहोस्_फाइल.py"""
import importlib as 가져오기
import sys as सञ्चालनप्रणाली_मान
from pathlib import Path as मार्ग
सञ्चालनप्रणाली_मान.path.insert(0, str(मार्ग(__file__).resolve().parents[1] / 'उपकरणहरू'))
if __name__ == '__main__':
    import runpy as अनुप्रयोग_कर्मचारी_अगुवा
    अनुप्रयोग_कर्मचारी_अगुवा.run_module('कार्यान्वयन_गर्नुहोस्_फाइल', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('कार्यान्वयन_गर्नुहोस्_फाइल')
    대응 = {'timeout': '시간제한', 's': 'स्ट्रिङ_लगत', 'i': '순번', 'match': '일치', 'files': 'फाइल_सूची', 'program': 'अनुप्रयोग', 'executable': '실행가능파일', 'args': 'तर्क_विन्यास', 'chunk': '조각', 'data': 'लगत', 'proc': 'प्रक्रिया', 'send': 'पठाउनुहोस्', 'main': 'चलाउनुहोस्', 'marker': '확인표시', 'command': 'आदेश', 'include': '포함항목', 'dumped': '갈무리자료', 'run': 'कार्यान्वयन_गर्नुहोस्_आदेश', 'p': 'लगत_राख्नुहोस्', 'parser': '인수해석기', 'options': 'विकल्पहरु', 'kind': 'कोटि_मान', 'selector': 'चयनकर्ता', 'upload_data': 'अपलोड_गर्नुहोस्_लगत', 'end': 'समाप्त_गर्नुहोस्_अफसेट', 'n': '개수', 'd': 'गन्तव्य_लगत', 'key': '누름값', 'output': '출력결과', 'line': 'रेखा', 'name': 'नाम', 'upload_name': 'अपलोड_गर्नुहोस्_नाम', 'receive': '수신하기'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
