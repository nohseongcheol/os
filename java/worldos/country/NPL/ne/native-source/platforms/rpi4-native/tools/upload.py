#!/usr/bin/env python3
"""기존 मार्ग 호환 प्रविष्टि_अंक. वास्तविक_लगत 구현: ../उपकरणहरू/अपलोड_गर्नुहोस्_फाइलहरू.py"""
import importlib as 가져오기
import sys as सञ्चालनप्रणाली_मान
from pathlib import Path as मार्ग
सञ्चालनप्रणाली_मान.path.insert(0, str(मार्ग(__file__).resolve().parents[1] / 'उपकरणहरू'))
if __name__ == '__main__':
    import runpy as अनुप्रयोग_कर्मचारी_अगुवा
    अनुप्रयोग_कर्मचारी_अगुवा.run_module('अपलोड_गर्नुहोस्_फाइलहरू', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('अपलोड_गर्नुहोस्_फाइलहरू')
    대응 = {'data': 'लगत', 'i': '순번', 'name': 'नाम', 'c': 'वर्ण_सङ्केत', 'p': 'लगत_राख्नुहोस्', 'args': 'तर्क_विन्यास'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
