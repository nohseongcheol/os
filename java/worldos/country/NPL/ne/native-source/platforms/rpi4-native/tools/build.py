#!/usr/bin/env python3
"""기존 मार्ग 호환 प्रविष्टि_अंक. वास्तविक_लगत 구현: ../उपकरणहरू/बनाउनुहोस्_प्रणाली.py"""
import importlib as 가져오기
import sys as सञ्चालनप्रणाली_मान
from pathlib import Path as मार्ग
सञ्चालनप्रणाली_मान.path.insert(0, str(मार्ग(__file__).resolve().parents[1] / 'उपकरणहरू'))
if __name__ == '__main__':
    import runpy as अनुप्रयोग_कर्मचारी_अगुवा
    अनुप्रयोग_कर्मचारी_अगुवा.run_module('बनाउनुहोस्_प्रणाली', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('बनाउनुहोस्_प्रणाली')
    대응 = {'network': 'सञ्जाल', 'BUILD': 'बनाउनुहोस्_बाटो', 'ar': 'सङ्ग्रह_उपकरण', 'build_examples': '예제만들기', 'posix': '포직스경로', 'font_data': 'फन्ट_लगत', 'flags': '설정비트', 'a': '첫째값', 'cc': '시언어번역기', 'args': 'तर्क_विन्यास', 'source_flags': '원본설정', 'ld': '연결편집기', 'method': 'तरिका_प्रविष्टि', 'main': 'चलाउनुहोस्', 'objcopy': 'वस्तु_फाइल_रुपान्तरणकर्ता', 'ROOT': 'परियोजना_रूट', 'cxx': '시플플번역기', 'includes': '포함인수', 'compiler': '번역기', 'build_users': 'सिर्जना_प्रयोगकर्ता_स्थान', 'f': 'फाइल_प्रविष्टि', 'extra': '추가영역', 'exports': 'निर्यात_गर्नुहोस्_तालिका', 'jobs': '빌드작업', 'run': 'कार्यान्वयन_गर्नुहोस्_आदेश', 'path': 'मार्ग', 'REPO': '저장소', 'tool': 'उपकरणहरू', 'classes': 'वर्ग_बाटो', 'output': '출력결과', 'samples': '예제들', 'symbol': 'चिन्ह_मान', 'source': '원본자료', 'name': 'नाम', 'build_network': 'सिर्जना_सञ्जाल_48d29d6d', 'font_info': 'फन्ट_जानकारी', 'manifest': '꾸러미명세', 'work': '작업경로'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
