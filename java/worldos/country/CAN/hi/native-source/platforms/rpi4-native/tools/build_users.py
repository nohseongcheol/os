#!/usr/bin/env python3
"""기존 पथ 호환 प्रवेश_बिदुं. वास्तविक_डेटा 구현: ../उपकरण/बिल्ड_उपयोगकर्ता_स्थान.py"""
import importlib as 가져오기
import sys as ऑपरेटिंग_सिस्टम_मान
from pathlib import Path as पथ
ऑपरेटिंग_सिस्टम_मान.path.insert(0, str(पथ(__file__).resolve().parents[1] / 'उपकरण'))
if __name__ == '__main__':
    import runpy as ऐप_लॉन्चर
    ऐप_लॉन्चर.run_module('बिल्ड_उपयोगकर्ता_स्थान', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('बिल्ड_उपयोगकर्ता_स्थान')
    대응 = {'mode': 'विधि_मोड', 'header': 'हेडर_मान', 'i': '순번', 'build_ccompiler': 'बनाएँ_सी_कंपाइलर', 'ar': 'संग्रह_उपकरण', 'posix': '포직스경로', 'payload': 'पेलोड_डेटा', 'flags': 'कॉन्फ़िगरेशन_बैकग्राउंड_इंटेलिजेंट_ट्रांसफ़र_सर्विस', 'cases': 'परिक्षण_विषय', 'cc': 'सी_कंपाइलर', 'data': 'आँकड़े', 'build_java_library': '자바라이브러리만들기', 'ld': '연결편집기', 'repo': 'संग्रह_पथ', 'build_python': '파이썬만들기', 'inc': '포함경로', 'argument': '전달값', 'text': 'पाठ', 'headers': 'हेडर_सूची', 'cxx': '시플플번역기', 'valid': 'वैध', 'build': 'बिल्ड', 'build_users': 'बनाएँ_उपयोगकर्ता_स्थान', 'compiler': 'कंपाइलर_उपकरण', 'uzlib': '압축해제경로', 'extra': '추가영역', 'phoff': 'ऐप_हेडर_ऑफ़सेट', 'offset': 'ऑफ़सेट_मान', 'text_address': 'आदेश_पता', 'abi': '호출규약', 'assembly': 'असेंबली', 'run': 'निष्पादित_करें_आदेश', 'path': 'पथ', 'p': 'डेटा_पद', 'changed': '바뀐자료', 'n': '개수', 'flag': 'सेटिंग_मान', 'index': 'लुकअप_इंडेक्स', 'classes': 'कक्षा_पथ', 'output': '출력결과', 'loads': '적재구획', 'data_address': 'डेटा_पता', 'symbol': 'प्रतीक_मान', 'root': 'मूल_पता', 'patches': '수정사항', 'source': '원본자료', 'sizes': '크기목록', 'blobs': '탑재덩이들', 'name': 'नाम', 'value': 'मान', 'fmt': 'डेटा_स्वरूप', 'work': '작업경로'}
    for 이전, अद्यतित_आइटम in 대응.items():
        if hasattr(구현, अद्यतित_आइटम): globals()[이전] = getattr(구현, अद्यतित_आइटम)
