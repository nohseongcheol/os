#!/usr/bin/env python3
"""기존 मार्ग 호환 प्रविष्टि_अंक. वास्तविक_लगत 구현: ../उपकरणहरू/कार्यान्वयन_गर्नुहोस्_आदेश.py"""
import importlib as 가져오기
import sys as सञ्चालनप्रणाली_मान
from pathlib import Path as मार्ग
सञ्चालनप्रणाली_मान.path.insert(0, str(मार्ग(__file__).resolve().parents[1] / 'उपकरणहरू'))
if __name__ == '__main__':
    import runpy as अनुप्रयोग_कर्मचारी_अगुवा
    अनुप्रयोग_कर्मचारी_अगुवा.run_module('कार्यान्वयन_गर्नुहोस्_आदेश', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('कार्यान्वयन_गर्नुहोस्_आदेश')
    대응 = {'supported': '지원목록', 'parser': '인수해석기', 'qemu': '모의기계', 'run_desktop': 'चलाउनुहोस्_डेस्कटप', 'main': 'चलाउनुहोस्', 'host': 'होस्ट', 'status': 'स्थिति_मान', 'NetworkBridge': 'सञ्जाल_ब्रिज', 'ROOT': 'परियोजना_रूट', 'bridge': 'ब्रिज', 'loader': '적재기', 'base': 'वालपेपर_मान', 'options': 'विकल्पहरु', 'binary': 'बाइनेरी', 'args': 'तर्क_विन्यास', 'command': 'आदेश'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
