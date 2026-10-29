#!/usr/bin/env python3
"""기존 گوزەر 호환 تێنووسین_خاڵ. ڕاستەکی_دەیتا 구현: ../ئامرازەکان/바탕화면시험.py"""
import importlib as 가져오기
import sys as سیستەمی_کارپێکردن_نرخ
from pathlib import Path as گوزەر
سیستەمی_کارپێکردن_نرخ.path.insert(0, str(گوزەر(__file__).resolve().parents[1] / 'ئامرازەکان'))
if __name__ == '__main__':
    import runpy as بەرنامە_ئەندامی_ستاف
    بەرنامە_ئەندامی_ستاف.run_module('바탕화면시험', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('바탕화면시험')
    대응 = {'x': 'پۆوتانی_x', 'typing': '글자입력', 'message': '알림문', 'start': 'ڕادان', 'down': '누르는중', 'exact': '정확한값', 'i': '순번', 'press': '글쇠누르기', 'rectangles': '사각형들', 'sym': 'سیمبۆل', 'j': '안쪽순번', 'deadline': '마감시각', 'proc': 'پرۆسە', 'data': 'دەیتا', 'main': 'ڕادان', 'w': '너비값', 'init': '초기값', 'block': 'دەیتا_بلۆک_کردن', 'ROOT': '기준', 'text': 'دەق', 'marker': '확인표시', 'report': 'ڕەواکردن_ڕاپۆرت', 'until': '까지', 'clipboard': 'ڕوونووسگە_نرخ', 'dst': 'جێمەبەست_ناونیشان', 'seen': '본항목들', 'poll': '준비살피미', 'transcript': '대화기록', 'port': '접속번호', 'offset': 'ئۆفسێت_نرخ', 'h': '높이값', 'src': '원본주소', 'event': 'پێشهات', 'encoding': 'کۆمەڵە_نووسە', 'size': 'گۆڕینی_ئەندازە', 'key': '누름값', 'pixels': '화소들', 'y': '세로좌표', 'output': '출력결과', 'symbol': 'سیمبۆل_نرخ', 'client': 'کلایەنت', 'char': 'نووسە_دەیتا', 'rgb': '빛삼원색'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
