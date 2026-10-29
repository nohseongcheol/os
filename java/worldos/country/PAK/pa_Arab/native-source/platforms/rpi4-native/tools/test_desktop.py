#!/usr/bin/env python3
"""기존 راہ 호환 داخلہ_مقام. اصلی_کوائف 구현: ../اوزار/바탕화면시험.py"""
import importlib as 가져오기
import sys as آپریٹنگ_سسٹم_قدر
from pathlib import Path as راہ
آپریٹنگ_سسٹم_قدر.path.insert(0, str(راہ(__file__).resolve().parents[1] / 'اوزار'))
if __name__ == '__main__':
    import runpy as ایپ_عملے_دا_رکن
    ایپ_عملے_دا_رکن.run_module('바탕화면시험', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('바탕화면시험')
    대응 = {'x': 'x_محدد', 'typing': '글자입력', 'message': '알림문', 'start': 'چلاؤ', 'down': '누르는중', 'exact': '정확한값', 'i': '순번', 'press': '글쇠누르기', 'rectangles': '사각형들', 'sym': 'علامت', 'j': '안쪽순번', 'deadline': '마감시각', 'proc': 'عمل', 'data': 'کوائف', 'main': 'چلاؤ', 'w': '너비값', 'init': '초기값', 'block': 'کوائف_بلاک', 'ROOT': '기준', 'text': 'متن', 'marker': '확인표시', 'report': 'جواز_دہی_رپورٹ', 'until': '까지', 'clipboard': 'تختہ_تراشہ_قدر', 'dst': 'منزل_مقصود_پتا', 'seen': '본항목들', 'poll': '준비살피미', 'transcript': '대화기록', 'port': '접속번호', 'offset': 'آف_سیٹ_قدر', 'h': '높이값', 'src': '원본주소', 'event': 'واقعہ', 'encoding': 'کریکٹر_سیٹ', 'size': 'سائز', 'key': '누름값', 'pixels': '화소들', 'y': '세로좌표', 'output': '출력결과', 'symbol': 'علامت_قدر', 'client': 'گاہک', 'char': 'کریکٹر_کوائف', 'rgb': '빛삼원색'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
