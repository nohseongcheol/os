#!/usr/bin/env python3
"""기존 பாதை_2 호환 நுழைவுப்_புள்ளி. அசல்_தரவு 구현: ../கருவிகள்/இயக்கு_கட்டளை.py"""
import importlib as 가져오기
import sys as இயக்க_முறைமை_மதிப்பு
from pathlib import Path as பாதை_2
இயக்க_முறைமை_மதிப்பு.path.insert(0, str(பாதை_2(__file__).resolve().parents[1] / 'கருவிகள்'))
if __name__ == '__main__':
    import runpy as நிரல்_துவக்குநர்
    நிரல்_துவக்குநர்.run_module('இயக்கு_கட்டளை', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('இயக்கு_கட்டளை')
    대응 = {'supported': '지원목록', 'parser': 'பார்சர்', 'qemu': '모의기계', 'run_desktop': 'இயக்கு_டெஸ்க்டாப்', 'main': 'செயல்படுத்துக', 'host': 'ஓம்பு', 'status': 'நிலை_மதிப்பு_e10195a1', 'NetworkBridge': 'பிணையம்_பிரிட்ஜ்', 'ROOT': 'திட்டப்பணி_மூலம்', 'bridge': 'பிரிட்ஜ்', 'loader': '적재기', 'base': 'பின்புல_மதிப்பு', 'options': 'விருப்பங்கள்', 'binary': 'பைனரி', 'args': 'மதிப்புரு_கோவை', 'command': 'கட்டளை'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
