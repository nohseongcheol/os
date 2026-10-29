#!/usr/bin/env python3
"""기존 पाथ 호환 प्रवेश_पॉयंट. प्रत्यक्ष_डेटा 구현: ../साधनां/दाळचे_प्रणाली.py"""
import importlib as TAKE_मोल
import sys as ऑपरेटिंग_प्रणाली_मोल
from pathlib import Path as पाथ
ऑपरेटिंग_प्रणाली_मोल.path.insert(0, str(पाथ(__file__).resolve().parents[1] / 'साधनां'))
if __name__ == '__main__':
    import runpy as एप्लिकेशन_ऍप्लिकेशन_ड्रॉवर
    एप्लिकेशन_ऍप्लिकेशन_ड्रॉवर.run_module('दाळचे_प्रणाली', run_name='__main__', alter_sys=True)
else:
    구현 = TAKE_मोल.import_module('दाळचे_प्रणाली')
    대응 = {'network': 'नॅटवर्क', 'BUILD': 'दाळचे_पाथ', 'ar': 'संग्रह_साधन', 'build_examples': '예제만들기', 'posix': '포직스경로', 'font_data': 'फाँट_डेटा', 'flags': '설정비트', 'a': '첫째값', 'cc': '시언어번역기', 'args': 'युक्तीवाद_क्रम', 'source_flags': '원본설정', 'ld': '연결편집기', 'method': 'पद्दत_प्रवेश', 'main': 'चलोवप', 'objcopy': 'ऑब्जॅक्ट_फायल_रूपांतर_करपी', 'ROOT': 'प्रॉजॅक्ट_रूट', 'cxx': '시플플번역기', 'includes': '포함인수', 'compiler': '번역기', 'build_users': 'निर्माण_करचें_उपेगकर्तो_SPACE', 'f': 'फायल_प्रवेश', 'extra': '추가영역', 'exports': 'निर्यात_तकटो', 'jobs': '빌드작업', 'run': 'पाळो_दिवचो_आदेश', 'path': 'पाथ', 'REPO': '저장소', 'tool': 'साधनां', 'classes': 'वर्ग_पाथ', 'output': '출력결과', 'samples': '예제들', 'symbol': 'चिन्न_मोल', 'source': '원본자료', 'name': 'नांव', 'build_network': 'निर्माण_करचें_नॅटवर्क', 'font_info': 'फाँट_म्हायती', 'manifest': '꾸러미명세', 'work': '작업경로'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
