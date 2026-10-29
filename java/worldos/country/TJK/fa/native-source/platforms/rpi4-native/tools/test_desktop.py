#!/usr/bin/env python3
"""기존 مسیر 호환 ورودی_نقطه. واقعی_داده_ها 구현: ../ابزارها/바탕화면시험.py"""
import importlib as 가져오기
import sys as سیستم_عامل_مقدار
from pathlib import Path as مسیر
سیستم_عامل_مقدار.path.insert(0, str(مسیر(__file__).resolve().parents[1] / 'ابزارها'))
if __name__ == '__main__':
    import runpy as برنامه_راه_انداز
    برنامه_راه_انداز.run_module('바탕화면시험', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('바탕화면시험')
    대응 = {'x': 'مختصات_x', 'typing': '글자입력', 'message': '알림문', 'start': 'اجرا_2', 'down': '누르는중', 'exact': '정확한값', 'i': '순번', 'press': 'فشار_دادن_کلید', 'rectangles': '사각형들', 'sym': 'نماد', 'j': '안쪽순번', 'deadline': '마감시각', 'proc': 'فرآیند', 'data': 'داده_ها', 'main': 'اجرا_2', 'w': '너비값', 'init': '초기값', 'block': 'داده_ها_مسدود_کردن', 'ROOT': 'نمایش_دادن_جذر', 'text': 'متن', 'marker': '확인표시', 'report': 'اعتبارسنجی_گزارش', 'until': '까지', 'clipboard': 'کلیپ_بورد_مقدار', 'dst': 'مقصد_آدرس', 'seen': '본항목들', 'poll': '준비살피미', 'transcript': '대화기록', 'port': 'شماره_درگاه', 'offset': 'جابجایی_لایه_ای_مقدار', 'h': '높이값', 'src': '원본주소', 'event': 'رویداد', 'encoding': 'مجموعه_نویسه_ها', 'size': 'اندازه', 'key': '누름값', 'pixels': '화소들', 'y': 'دکمه_Y_مختصات', 'output': '출력결과', 'symbol': 'نماد_مقدار', 'client': 'سرویس_گیرنده', 'char': 'نویسه_داده_ها', 'rgb': '빛삼원색'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
