#!/usr/bin/env python3
"""기존 मार्ग 호환 प्रविष्टि_अंक. वास्तविक_लगत 구현: ../उपकरणहरू/बनाउनुहोस्_प्रयोगकर्ता_स्थान.py"""
import importlib as 가져오기
import sys as सञ्चालनप्रणाली_मान
from pathlib import Path as मार्ग
सञ्चालनप्रणाली_मान.path.insert(0, str(मार्ग(__file__).resolve().parents[1] / 'उपकरणहरू'))
if __name__ == '__main__':
    import runpy as अनुप्रयोग_कर्मचारी_अगुवा
    अनुप्रयोग_कर्मचारी_अगुवा.run_module('बनाउनुहोस्_प्रयोगकर्ता_स्थान', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('बनाउनुहोस्_प्रयोगकर्ता_स्थान')
    대응 = {'mode': 'तरिका_मोड', 'header': 'हेडर_मान', 'i': '순번', 'build_ccompiler': '시언어번역기만들기', 'ar': 'सङ्ग्रह_उपकरण', 'posix': '포직스경로', 'payload': 'पेलोड_लगत', 'flags': '설정비트', 'cases': '시험사례', 'cc': '시언어번역기', 'data': 'लगत', 'build_java_library': '자바라이브러리만들기', 'ld': '연결편집기', 'repo': '저장소경로', 'build_python': '파이썬만들기', 'inc': '포함경로', 'argument': '전달값', 'text': 'पाठ', 'headers': 'हेडर_सूची', 'cxx': '시플플번역기', 'valid': '유효함', 'build': 'बनाउनुहोस्', 'build_users': 'सिर्जना_प्रयोगकर्ता_स्थान', 'compiler': '번역기', 'uzlib': '압축해제경로', 'extra': '추가영역', 'phoff': 'अनुप्रयोग_हेडर_अफसेट', 'offset': 'अफसेट_मान', 'text_address': 'आदेश_ठेगाना', 'abi': '호출규약', 'assembly': '어셈블리자료', 'run': 'कार्यान्वयन_गर्नुहोस्_आदेश', 'path': 'मार्ग', 'p': 'लगत_राख्नुहोस्', 'changed': '바뀐자료', 'n': '개수', 'flag': 'सेटिङहरू_मान', 'index': 'विवरण_हेर्ने_सुविधा_अनुक्रमणिका', 'classes': 'वर्ग_बाटो', 'output': '출력결과', 'loads': '적재구획', 'data_address': 'लगत_ठेगाना', 'symbol': 'चिन्ह_मान', 'root': 'रूट_ठेगाना', 'patches': '수정사항', 'source': '원본자료', 'sizes': '크기목록', 'blobs': '탑재덩이들', 'name': 'नाम', 'value': 'मान', 'fmt': 'स्वरूप', 'work': '작업경로'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
