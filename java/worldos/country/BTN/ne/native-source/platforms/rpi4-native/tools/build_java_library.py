#!/usr/bin/env python3
"""기존 मार्ग 호환 प्रविष्टि_अंक. वास्तविक_लगत 구현: ../उपकरणहरू/자바라이브러리빌드.py"""
import importlib as 가져오기
import sys as सञ्चालनप्रणाली_मान
from pathlib import Path as मार्ग
सञ्चालनप्रणाली_मान.path.insert(0, str(मार्ग(__file__).resolve().parents[1] / 'उपकरणहरू'))
if __name__ == '__main__':
    import runpy as अनुप्रयोग_कर्मचारी_अगुवा
    अनुप्रयोग_कर्मचारी_अगुवा.run_module('자바라이브러리빌드', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('자바라이브러리빌드')
    대응 = {'header': 'हेडर_मान', 'sources': '원문목록', 'i': '순번', 'info': 'प्रणाली_जानकारी', 'payload': 'पेलोड_लगत', 'src': '원본주소', 'run': 'कार्यान्वयन_गर्नुहोस्_आदेश', 'build_java_library': '자바라이브러리만들기', 'relative': '상대경로', 'classes': 'वर्ग_बाटो', 'dist': '배포경로', 'archive': 'सङ्ग्रह', 'output': '출력결과', 'root': 'रूट_ठेगाना', 'name': 'नाम', 'jar': '자바꾸러미', 'b': '둘째값', 'entries': '항목들'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
