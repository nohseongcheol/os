#!/usr/bin/env python3
"""기존 பாதை_2 호환 நுழைவுப்_புள்ளி. அசல்_தரவு 구현: ../கருவிகள்/இயக்கு_கோப்பு.py"""
import importlib as 가져오기
import sys as இயக்க_முறைமை_மதிப்பு
from pathlib import Path as பாதை_2
இயக்க_முறைமை_மதிப்பு.path.insert(0, str(பாதை_2(__file__).resolve().parents[1] / 'கருவிகள்'))
if __name__ == '__main__':
    import runpy as நிரல்_துவக்குநர்
    நிரல்_துவக்குநர்.run_module('இயக்கு_கோப்பு', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('இயக்கு_கோப்பு')
    대응 = {'timeout': '시간제한', 's': 'சரம்_தரவு', 'i': '순번', 'match': '일치', 'files': 'கோப்பு_பட்டியல்', 'program': 'நிரல்', 'executable': 'செயல்படுத்தக்கூடிய_கோப்பு_படம்', 'args': 'மதிப்புரு_கோவை', 'chunk': '조각', 'data': 'தரவு', 'proc': 'செயல்பாடு', 'send': 'அனுப்பு', 'main': 'செயல்படுத்துக', 'marker': '확인표시', 'command': 'கட்டளை', 'include': '포함항목', 'dumped': '갈무리자료', 'run': 'இயக்கு_கட்டளை', 'p': 'தரவு_நிலை', 'parser': 'பார்சர்', 'options': 'விருப்பங்கள்', 'kind': 'வகை_மதிப்பு_4b6d6445', 'selector': 'தேர்வி', 'upload_data': 'பதிவேற்று_தரவு', 'end': 'முடி_ஆஃப்செட்', 'n': '개수', 'd': 'இலக்கு_தரவு', 'key': '누름값', 'output': '출력결과', 'line': 'உள்ளீட்டு_வரி', 'name': 'பெயர்', 'upload_name': 'பதிவேற்று_பெயர்', 'receive': '수신하기'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
