#!/usr/bin/env python3
"""기존 பாதை_2 호환 நுழைவுப்_புள்ளி. அசல்_தரவு 구현: ../கருவிகள்/바탕화면시험.py"""
import importlib as 가져오기
import sys as இயக்க_முறைமை_மதிப்பு
from pathlib import Path as பாதை_2
இயக்க_முறைமை_மதிப்பு.path.insert(0, str(பாதை_2(__file__).resolve().parents[1] / 'கருவிகள்'))
if __name__ == '__main__':
    import runpy as நிரல்_துவக்குநர்
    நிரல்_துவக்குநர்.run_module('바탕화면시험', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('바탕화면시험')
    대응 = {'x': 'x_ஒத்ததரமுள்ளது', 'typing': '글자입력', 'message': '알림문', 'start': 'செயல்படுத்துக', 'down': '누르는중', 'exact': '정확한값', 'i': '순번', 'press': '글쇠누르기', 'rectangles': '사각형들', 'sym': 'சின்னம்', 'j': '안쪽순번', 'deadline': '마감시각', 'proc': 'செயல்பாடு', 'data': 'தரவு', 'main': 'செயல்படுத்துக', 'w': '너비값', 'init': '초기값', 'block': 'தரவு_தடு', 'ROOT': 'திட்டப்பணி_மூலம்', 'text': 'உரை', 'marker': '확인표시', 'report': 'செல்லுபடியாக்கம்_அறிக்கை', 'until': '까지', 'clipboard': 'நகலகம்_மதிப்பு', 'dst': 'இலக்கு_முகவரி_08bbd577', 'seen': '본항목들', 'poll': '준비살피미', 'transcript': '대화기록', 'port': 'முனைய_எண்', 'offset': 'ஆஃப்செட்_மதிப்பு', 'h': '높이값', 'src': '원본주소', 'event': 'நிகழ்வு', 'encoding': 'எழுத்துக்குறி_குழு', 'size': 'அளவு', 'key': '누름값', 'pixels': '화소들', 'y': 'Y_பொத்தான்_அச்சுத்_தொகுப்பு', 'output': '출력결과', 'symbol': 'சின்னம்_மதிப்பு', 'client': 'பயனகம்', 'char': 'எழுத்துருத்_தரவு', 'rgb': '빛삼원색'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
