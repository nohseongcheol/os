#!/usr/bin/env python3
"""기존 راستہ_2 호환 اندراج_نقطہ. اصل_کوائف 구현: ../ٹولز/바탕화면시험.py"""
import importlib as 가져오기
import sys as آپریٹنگ_سسٹم_قدر
from pathlib import Path as راستہ_2
آپریٹنگ_سسٹم_قدر.path.insert(0, str(راستہ_2(__file__).resolve().parents[1] / 'ٹولز'))
if __name__ == '__main__':
    import runpy as ایپ_ایپ_دراز
    ایپ_ایپ_دراز.run_module('바탕화면시험', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('바탕화면시험')
    대응 = {'x': 'ایکس_مربوط', 'typing': '글자입력', 'message': '알림문', 'start': 'چلائیں', 'down': '누르는중', 'exact': '정확한값', 'i': '순번', 'press': '글쇠누르기', 'rectangles': '사각형들', 'sym': 'علامت', 'j': '안쪽순번', 'deadline': '마감시각', 'proc': 'عمل_کاری', 'data': 'کوائف', 'main': 'چلائیں', 'w': '너비값', 'init': '초기값', 'block': 'کوائف_بلاک_کریں', 'ROOT': 'عکس_ڈالنا_روٹ', 'text': 'متن', 'marker': '확인표시', 'report': 'توثیق_رپورٹ', 'until': '까지', 'clipboard': 'تختہ_تراشہ_قدر', 'dst': 'منزل_مقصود_پتہ', 'seen': '본항목들', 'poll': '준비살피미', 'transcript': '대화기록', 'port': 'دہانہ_نمبر', 'offset': 'آفسٹ_قدر', 'h': '높이값', 'src': '원본주소', 'event': 'واقعہ', 'encoding': 'کریکٹر_سیٹ', 'size': 'حجم', 'key': '누름값', 'pixels': '화소들', 'y': '세로좌표', 'output': '출력결과', 'symbol': 'علامت_قدر', 'client': 'کلائنٹ', 'char': 'کریکٹر_کوائف', 'rgb': '빛삼원색'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
