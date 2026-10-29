#!/usr/bin/env python3
"""기존 मार्ग 호환 प्रविष्टि_अंक. वास्तविक_लगत 구현: ../उपकरणहरू/बनाउनुहोस्_सञ्जाल.py"""
import importlib as 가져오기
import sys as सञ्चालनप्रणाली_मान
from pathlib import Path as मार्ग
सञ्चालनप्रणाली_मान.path.insert(0, str(मार्ग(__file__).resolve().parents[1] / 'उपकरणहरू'))
if __name__ == '__main__':
    import runpy as अनुप्रयोग_कर्मचारी_अगुवा
    अनुप्रयोग_कर्मचारी_अगुवा.run_module('बनाउनुहोस्_सञ्जाल', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('बनाउनुहोस्_सञ्जाल')
    대응 = {'obj': 'गन्तव्य_फाइल', 'objects': 'गन्तव्य_फाइलहरू', 'library': 'पुस्तकालय', 'output': '출력결과', 'port': '접속번호', 'root': 'रूट_ठेगाना', 'files': 'फाइल_सूची', 'source': '원본자료', 'run': 'कार्यान्वयन_गर्नुहोस्_आदेश', 'flags': '설정비트', 'path': 'मार्ग', 'build_network': 'सिर्जना_सञ्जाल_48d29d6d', 'cc': '시언어번역기', 'ar': 'सङ्ग्रह_उपकरण'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
