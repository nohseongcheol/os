#!/usr/bin/env python3
"""기존 मार्ग 호환 प्रविष्टि_अंक. वास्तविक_लगत 구현: ../उपकरणहरू/예제빌드.py"""
import importlib as 가져오기
import sys as सञ्चालनप्रणाली_मान
from pathlib import Path as मार्ग
सञ्चालनप्रणाली_मान.path.insert(0, str(मार्ग(__file__).resolve().parents[1] / 'उपकरणहरू'))
if __name__ == '__main__':
    import runpy as अनुप्रयोग_कर्मचारी_अगुवा
    अनुप्रयोग_कर्मचारी_अगुवा.run_module('예제빌드', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('예제빌드')
    대응 = {'out': 'मापन_लगत', 'build_examples': '예제만들기', 'files': 'फाइल_सूची', 'java': '자바실행', 'run': 'कार्यान्वयन_गर्नुहोस्_आदेश', 'path': 'मार्ग', 'p': 'लगत_राख्नुहोस्', 'readme': 'readme_फाइल', 'build_java_library': '자바라이브러리만들기', 'code': '명령열', 'index': 'विवरण_हेर्ने_सुविधा_अनुक्रमणिका', 'classes': 'वर्ग_बाटो', 'repo': '저장소경로', 'root': 'रूट_ठेगाना', 'content': 'सामग्री_मान', 'source': '원본자료', 'name': 'नाम', 'target': 'लक्ष्य', 'manifest': '꾸러미명세', 'language': 'भाषा'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
