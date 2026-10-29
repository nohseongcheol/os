#!/usr/bin/env python3
"""기존 பாதை_2 호환 நுழைவுப்_புள்ளி. அசல்_தரவு 구현: ../கருவிகள்/பதிவேற்று_கோப்புகள்.py"""
import importlib as 가져오기
import sys as இயக்க_முறைமை_மதிப்பு
from pathlib import Path as பாதை_2
இயக்க_முறைமை_மதிப்பு.path.insert(0, str(பாதை_2(__file__).resolve().parents[1] / 'கருவிகள்'))
if __name__ == '__main__':
    import runpy as நிரல்_துவக்குநர்
    நிரல்_துவக்குநர்.run_module('பதிவேற்று_கோப்புகள்', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('பதிவேற்று_கோப்புகள்')
    대응 = {'data': 'தரவு', 'i': '순번', 'name': 'பெயர்', 'c': 'எழுத்துக்குறி_குறியீடு', 'p': 'தரவு_நிலை', 'args': 'மதிப்புரு_கோவை'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
