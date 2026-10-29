#!/usr/bin/env python3
"""기존 பாதை_2 호환 நுழைவுப்_புள்ளி. அசல்_தரவு 구현: ../கருவிகள்/되돌림시험서버.py"""
import importlib as 가져오기
import sys as இயக்க_முறைமை_மதிப்பு
from pathlib import Path as பாதை_2
இயக்க_முறைமை_மதிப்பு.path.insert(0, str(பாதை_2(__file__).resolve().parents[1] / 'கருவிகள்'))
if __name__ == '__main__':
    import runpy as நிரல்_துவக்குநர்
    நிரல்_துவக்குநர்.run_module('되돌림시험서버', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('되돌림시험서버')
    대응 = {'data': 'தரவு', 'e': '보조항목', 'connection': 'இணைப்பு_e05f319b', 'f': 'கோப்பு_உள்ளீடு', 'peer': 'பியர்_மதிப்பு', 'self': '자신', 'udp': '전문제어', 't': 'முனையம்_உள்ளீடு', 'tcp': 'இணைப்பு_கட்டுப்பாடு', 'EchoFixture': '되돌림시험서버', 'args': 'மதிப்புரு_கோவை', 'chunk': '조각'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
