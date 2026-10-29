#!/usr/bin/env python3
"""기존 பாதை_2 호환 நுழைவுப்_புள்ளி. அசல்_தரவு 구현: ../கருவிகள்/개발꾸러미내보내기.py"""
import importlib as 가져오기
import sys as இயக்க_முறைமை_மதிப்பு
from pathlib import Path as பாதை_2
இயக்க_முறைமை_மதிப்பு.path.insert(0, str(பாதை_2(__file__).resolve().parents[1] / 'கருவிகள்'))
if __name__ == '__main__':
    import runpy as நிரல்_துவக்குநர்
    நிரல்_துவக்குநர்.run_module('개발꾸러미내보내기', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('개발꾸러미내보내기')
    대응 = {'out': 'அளவிடக்கூடியது_தரவு', 'obj': 'இலக்குக்_கோப்பு', 'relative': 'தொடர்புடைய_பாதை', 'compiler_archive': '번역기꾸러미', 'sdk': '개발꾸러미', 'dist': '배포경로', 'archive': 'காப்பகம்', 'main': 'செயல்படுத்துக', 'posix': '포직스경로', 'files': 'கோப்பு_பட்டியல்', 'source': '원본자료', 'name': 'பெயர்', 'target': 'இலக்கு', 'ROOT': 'திட்டப்பணி_மூலம்', 'destination': 'இலக்கு_தரவு_முகவரி', 'manifest': 'மூட்டை_தொற்றம்', 'work': '작업경로'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
