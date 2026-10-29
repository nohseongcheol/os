#!/usr/bin/env python3
"""기존 பாதை_2 호환 நுழைவுப்_புள்ளி. அசல்_தரவு 구현: ../கருவிகள்/셸시험.py"""
import importlib as 가져오기
import sys as இயக்க_முறைமை_மதிப்பு
from pathlib import Path as பாதை_2
இயக்க_முறைமை_மதிப்பு.path.insert(0, str(பாதை_2(__file__).resolve().parents[1] / 'கருவிகள்'))
if __name__ == '__main__':
    import runpy as நிரல்_துவக்குநர்
    நிரல்_துவக்குநர்.run_module('셸시험', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('셸시험')
    대응 = {'timeout': '시간제한', 'x': 'x_ஒத்ததரமுள்ளது', 'msg': 'பிணையம்_செய்தி', 'i': '순번', 'reply': 'பதிலளி', 'call': '호출', 'args': 'மதிப்புரு_கோவை', 'chunk': '조각', 'data': 'தரவு', 'proc': 'செயல்பாடு', 'long_text': '긴글', 'restored': '복원자료', 'send': 'அனுப்பு', 'file': 'கோப்பின்_பெயர்', 'main': 'செயல்படுத்துக', 'found': 'தேடு_அளவிடக்கூடியது', 'ROOT': 'திட்டப்பணி_மூலம்', 'text': 'உரை', 'marker': '확인표시', 'command': 'கட்டளை', 'expected': '예상결과', 'pixel': 'படக்_கூறு', 'shell': 'கூடு', 'poll': '준비살피미', 'transcript': '대화기록', 'end': 'முடி_ஆஃப்செட்', 'image': 'படம்', 'key': '누름값', 'y': 'Y_பொத்தான்_அச்சுத்_தொகுப்பு', 'output': '출력결과', 'result': 'அளவிடக்கூடியது', 'client': 'பயனகம்', 'line': 'உள்ளீட்டு_வரி', 'stream': 'தொடரோடி_மதிப்பு', 'name': 'பெயர்', 'value': 'மதிப்பு', 'receive': '수신하기', 'report': 'செல்லுபடியாக்கம்_அறிக்கை', 'work': '작업경로', 'qmp': '모의제어접속'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
