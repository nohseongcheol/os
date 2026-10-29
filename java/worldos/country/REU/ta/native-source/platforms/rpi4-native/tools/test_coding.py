#!/usr/bin/env python3
"""기존 பாதை_2 호환 நுழைவுப்_புள்ளி. அசல்_தரவு 구현: ../கருவிகள்/코딩시험.py"""
import importlib as 가져오기
import sys as இயக்க_முறைமை_மதிப்பு
from pathlib import Path as பாதை_2
இயக்க_முறைமை_மதிப்பு.path.insert(0, str(பாதை_2(__file__).resolve().parents[1] / 'கருவிகள்'))
if __name__ == '__main__':
    import runpy as நிரல்_துவக்குநர்
    நிரல்_துவக்குநர்.run_module('코딩시험', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('코딩시험')
    대응 = {'out': 'அளவிடக்கூடியது_தரவு', 'expected': '예상결과', 'sdk': '개발꾸러미', 'suffix': '뒷부분', 'arc': '압축묶음', 'main': 'செயல்படுத்துக', 'elf': 'செயல்படுத்தக்கூடிய_கோப்பு', 'run': 'இயக்கு_கட்டளை', 'name': 'பெயர்', 'path': 'பாதை_2', 'p': 'தரவு_நிலை', 'ROOT': 'திட்டப்பணி_மூலம்', 'report': 'செல்லுபடியாக்கம்_அறிக்கை', 'args': 'மதிப்புரு_கோவை'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
