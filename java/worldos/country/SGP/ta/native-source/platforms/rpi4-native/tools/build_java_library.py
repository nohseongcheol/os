#!/usr/bin/env python3
"""기존 பாதை_2 호환 நுழைவுப்_புள்ளி. அசல்_தரவு 구현: ../கருவிகள்/자바라이브러리빌드.py"""
import importlib as 가져오기
import sys as இயக்க_முறைமை_மதிப்பு
from pathlib import Path as பாதை_2
இயக்க_முறைமை_மதிப்பு.path.insert(0, str(பாதை_2(__file__).resolve().parents[1] / 'கருவிகள்'))
if __name__ == '__main__':
    import runpy as நிரல்_துவக்குநர்
    நிரல்_துவக்குநர்.run_module('자바라이브러리빌드', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('자바라이브러리빌드')
    대응 = {'header': 'மேற்குறிப்பு_மதிப்பு', 'sources': '원문목록', 'i': '순번', 'info': 'கணினித்_தகவல்', 'payload': 'பேலோட்_தரவு', 'src': '원본주소', 'run': 'இயக்கு_கட்டளை', 'build_java_library': '자바라이브러리만들기', 'relative': 'தொடர்புடைய_பாதை', 'classes': 'பிரிவு_பாதை', 'dist': '배포경로', 'archive': 'காப்பகம்', 'output': '출력결과', 'root': 'மூலம்_முகவரி', 'name': 'பெயர்', 'jar': '자바꾸러미', 'b': '둘째값', 'entries': '항목들'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
