#!/usr/bin/env python3
"""기존 मार्ग 호환 प्रविष्टि_अंक. वास्तविक_लगत 구현: ../उपकरणहरू/시언어번역기빌드.py"""
import importlib as 가져오기
import sys as सञ्चालनप्रणाली_मान
from pathlib import Path as मार्ग
सञ्चालनप्रणाली_मान.path.insert(0, str(मार्ग(__file__).resolve().parents[1] / 'उपकरणहरू'))
if __name__ == '__main__':
    import runpy as अनुप्रयोग_कर्मचारी_अगुवा
    अनुप्रयोग_कर्मचारी_अगुवा.run_module('시언어번역기빌드', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('시언어번역기빌드')
    대응 = {'out': 'मापन_लगत', 'builtins': '내장연산', 'header': 'हेडर_मान', 'sdk': '개발꾸러미', 'build_ccompiler': '시언어번역기만들기', 'i': '순번', 'elf': '실행파일', 'run': 'कार्यान्वयन_गर्नुहोस्_आदेश', 'flags': '설정비트', 'path': 'मार्ग', 'p': 'लगत_राख्नुहोस्', 'cc': '시언어번역기', 'obj': 'गन्तव्य_फाइल', 'flag': 'सेटिङहरू_मान', 'ld': '연결편집기', 'objects': 'गन्तव्य_फाइलहरू', 'repo': '저장소경로', 'v': '임시값', 'upstream': '외부원문', 'root': 'रूट_ठेगाना', 'assets': '탑재자료', 'source': '원본자료', 'name': 'नाम', 'includes': '포함인수'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
