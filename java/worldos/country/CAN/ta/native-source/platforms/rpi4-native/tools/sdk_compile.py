#!/usr/bin/env python3
"""기존 பாதை_2 호환 நுழைவுப்_புள்ளி. அசல்_தரவு 구현: ../கருவிகள்/개발꾸러미번역.py"""
import importlib as 가져오기
import sys as இயக்க_முறைமை_மதிப்பு
from pathlib import Path as பாதை_2
இயக்க_முறைமை_மதிப்பு.path.insert(0, str(பாதை_2(__file__).resolve().parents[1] / 'கருவிகள்'))
if __name__ == '__main__':
    import runpy as நிரல்_துவக்குநர்
    நிரல்_துவக்குநர்.run_module('개발꾸러미번역', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('개발꾸러미번역')
    대응 = {'compiler': '번역기', 'obj': 'இலக்குக்_கோப்பு', 'sdk': '개발꾸러미', 'output': '출력결과', 'main': 'செயல்படுத்துக', 'elf': 'செயல்படுத்தக்கூடிய_கோப்பு', 'is_c': '시언어여부', 'parser': 'பார்சர்', 'language': 'மொழி', 'work': '작업경로', 'args': 'மதிப்புரு_கோவை'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
