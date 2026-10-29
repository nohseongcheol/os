#!/usr/bin/env python3
"""기존 पाथ 호환 प्रवेश_पॉयंट. प्रत्यक्ष_डेटा 구현: ../साधनां/दाळचे_उपेगकर्तो_SPACE.py"""
import importlib as TAKE_मोल
import sys as ऑपरेटिंग_प्रणाली_मोल
from pathlib import Path as पाथ
ऑपरेटिंग_प्रणाली_मोल.path.insert(0, str(पाथ(__file__).resolve().parents[1] / 'साधनां'))
if __name__ == '__main__':
    import runpy as एप्लिकेशन_ऍप्लिकेशन_ड्रॉवर
    एप्लिकेशन_ऍप्लिकेशन_ड्रॉवर.run_module('दाळचे_उपेगकर्तो_SPACE', run_name='__main__', alter_sys=True)
else:
    구현 = TAKE_मोल.import_module('दाळचे_उपेगकर्तो_SPACE')
    대응 = {'mode': 'पद्दत_मोड', 'header': 'माथाळो_मोल', 'i': '순번', 'build_ccompiler': '시언어번역기만들기', 'ar': 'संग्रह_साधन', 'posix': '포직스경로', 'payload': 'पेलोड_डेटा', 'flags': '설정비트', 'cases': '시험사례', 'cc': '시언어번역기', 'data': 'डेटा', 'build_java_library': '자바라이브러리만들기', 'ld': '연결편집기', 'repo': '저장소경로', 'build_python': 'निर्माण_करचें_PYTHON', 'inc': '포함경로', 'argument': '전달값', 'text': 'SMS', 'headers': 'माथाळो_सुची', 'cxx': '시플플번역기', 'valid': '유효함', 'build': 'दाळचे', 'build_users': 'निर्माण_करचें_उपेगकर्तो_SPACE', 'compiler': '번역기', 'uzlib': '압축해제경로', 'extra': '추가영역', 'phoff': 'एप्लिकेशन_माथाळो_ऑफसॅट', 'offset': 'ऑफसॅट_मोल', 'text_address': 'आदेश_नामो', 'abi': '호출규약', 'assembly': '어셈블리자료', 'run': 'पाळो_दिवचो_आदेश', 'path': 'पाथ', 'p': 'डेटा_स्थिती', 'changed': '바뀐자료', 'n': 'आयटम_COUNT', 'flag': 'मांडावळी_मोल', 'index': 'लूकअप_INDEX', 'classes': 'वर्ग_पाथ', 'output': '출력결과', 'loads': '적재구획', 'data_address': 'डेटा_नामो', 'symbol': 'चिन्न_मोल', 'root': 'रूट_नामो', 'patches': '수정사항', 'source': '원본자료', 'sizes': '크기목록', 'blobs': '탑재덩이들', 'name': 'नांव', 'value': 'मोल', 'fmt': 'स्वरूप_932e03c8', 'work': '작업경로'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
