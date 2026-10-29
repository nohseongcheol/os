#!/usr/bin/env python3
"""기존 பாதை_2 호환 நுழைவுப்_புள்ளி. அசல்_தரவு 구현: ../கருவிகள்/예제빌드.py"""
import importlib as 가져오기
import sys as இயக்க_முறைமை_மதிப்பு
from pathlib import Path as பாதை_2
இயக்க_முறைமை_மதிப்பு.path.insert(0, str(பாதை_2(__file__).resolve().parents[1] / 'கருவிகள்'))
if __name__ == '__main__':
    import runpy as நிரல்_துவக்குநர்
    நிரல்_துவக்குநர்.run_module('예제빌드', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('예제빌드')
    대응 = {'out': 'அளவிடக்கூடியது_தரவு', 'build_examples': '예제만들기', 'files': 'கோப்பு_பட்டியல்', 'java': '자바실행', 'run': 'இயக்கு_கட்டளை', 'path': 'பாதை_2', 'p': 'தரவு_நிலை', 'readme': 'பயனர்_உதவிக்_கோப்பு', 'build_java_library': '자바라이브러리만들기', 'code': '명령열', 'index': 'தேடுதல்_அடைவு', 'classes': 'பிரிவு_பாதை', 'repo': 'தொகுபதிவகம்_பாதை', 'root': 'மூலம்_முகவரி', 'content': 'உள்ளடக்கம்_மதிப்பு', 'source': '원본자료', 'name': 'பெயர்', 'target': 'இலக்கு', 'manifest': 'மூட்டை_தொற்றம்', 'language': 'மொழி'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
