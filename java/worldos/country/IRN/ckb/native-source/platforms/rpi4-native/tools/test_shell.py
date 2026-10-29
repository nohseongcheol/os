#!/usr/bin/env python3
"""기존 گوزەر 호환 تێنووسین_خاڵ. ڕاستەکی_دەیتا 구현: ../ئامرازەکان/셸시험.py"""
import importlib as 가져오기
import sys as سیستەمی_کارپێکردن_نرخ
from pathlib import Path as گوزەر
سیستەمی_کارپێکردن_نرخ.path.insert(0, str(گوزەر(__file__).resolve().parents[1] / 'ئامرازەکان'))
if __name__ == '__main__':
    import runpy as بەرنامە_ئەندامی_ستاف
    بەرنامە_ئەندامی_ستاف.run_module('셸시험', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('셸시험')
    대응 = {'timeout': '시간제한', 'x': 'پۆوتانی_x', 'msg': 'تۆڕ_پەیام', 'i': '순번', 'reply': 'وەڵامدانەوه', 'call': '호출', 'args': 'ئارگیومێنت_ڕیزی_داتا', 'chunk': '조각', 'data': 'دەیتا', 'proc': 'پرۆسە', 'long_text': '긴글', 'restored': '복원자료', 'send': 'ناردن', 'file': 'فایل', 'main': 'ڕادان', 'found': '찾은결과', 'ROOT': '기준', 'text': 'دەق', 'marker': '확인표시', 'command': 'فەرمان', 'expected': '예상결과', 'pixel': 'پێڵ', 'shell': 'توێکڵ', 'poll': '준비살피미', 'transcript': '대화기록', 'end': 'دوایی_کردن_ئۆفسێت', 'image': 'وێنە', 'key': '누름값', 'y': '세로좌표', 'output': '출력결과', 'result': '결과', 'client': 'کلایەنت', 'line': 'دێڕ', 'stream': 'Stream_نرخ', 'name': 'ناو', 'value': 'نرخ', 'receive': '수신하기', 'report': 'ڕەواکردن_ڕاپۆرت', 'work': '작업경로', 'qmp': '모의제어접속'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
