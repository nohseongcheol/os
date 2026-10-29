#!/usr/bin/env python3
"""기존 பாதை_2 호환 நுழைவுப்_புள்ளி. அசல்_தரவு 구현: ../கருவிகள்/시언어번역기빌드.py"""
import importlib as 가져오기
import sys as இயக்க_முறைமை_மதிப்பு
from pathlib import Path as பாதை_2
இயக்க_முறைமை_மதிப்பு.path.insert(0, str(பாதை_2(__file__).resolve().parents[1] / 'கருவிகள்'))
if __name__ == '__main__':
    import runpy as நிரல்_துவக்குநர்
    நிரல்_துவக்குநர்.run_module('시언어번역기빌드', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('시언어번역기빌드')
    대응 = {'out': 'அளவிடக்கூடியது_தரவு', 'builtins': '내장연산', 'header': 'மேற்குறிப்பு_மதிப்பு', 'sdk': '개발꾸러미', 'build_ccompiler': '시언어번역기만들기', 'i': '순번', 'elf': 'செயல்படுத்தக்கூடிய_கோப்பு', 'run': 'இயக்கு_கட்டளை', 'flags': 'உள்ளமைவு_பின்புல_நுண்ணறிவு_டிரான்ஸ்ஃபர்_சேவை', 'path': 'பாதை_2', 'p': 'தரவு_நிலை', 'cc': '시언어번역기', 'obj': 'இலக்குக்_கோப்பு', 'flag': 'அமைப்புகள்_மதிப்பு', 'ld': '연결편집기', 'objects': 'இலக்கு_கோப்புகள்', 'repo': 'தொகுபதிவகம்_பாதை', 'v': '임시값', 'upstream': 'அப்ஸ்ட்ரீம்', 'root': 'மூலம்_முகவரி', 'assets': '탑재자료', 'source': '원본자료', 'name': 'பெயர்', 'includes': '포함인수'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
