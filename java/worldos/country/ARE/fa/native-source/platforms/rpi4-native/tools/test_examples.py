#!/usr/bin/env python3
"""기존 مسیر 호환 ورودی_نقطه. واقعی_داده_ها 구현: ../ابزارها/예제시험.py"""
import importlib as 가져오기
import sys as سیستم_عامل_مقدار
from pathlib import Path as مسیر
سیستم_عامل_مقدار.path.insert(0, str(مسیر(__file__).resolve().parents[1] / 'ابزارها'))
if __name__ == '__main__':
    import runpy as برنامه_راه_انداز
    برنامه_راه_انداز.run_module('예제시험', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('예제시험')
    대응 = {'count': '항목수', 'exact': '정확한값', 'expected_file': '예상파일', 'ftp_port': 'فایل_انتقال_شماره_درگاه', 'data': 'داده_ها', 'graphics_command': 'گرافیک_ها_فرمان', 'main': 'اجرا_2', 'row': 'ردیف_مرتب_کردن', 'init': '초기값', 'target': 'هدف', 'ROOT': 'نمایش_دادن_جذر', 'text': 'متن', 'binary': 'دودویی', 'out': 'سنجش_داده_ها', 'entry': 'ورودی_نقطه', 'got': '받은수', 'port': 'شماره_درگاه', 'graphics_start': 'شروع_نقاشی', 'col': 'ستون_مرتب_کردن', 'begin': 'شروع_جابجایی_لایه_ای', 'kind': 'دسته_مقدار', 'selector': 'انتخاب_کننده', 'n': '개수', 'key': '누름값', 'y': 'دکمه_Y_مختصات', 'client': 'سرویس_گیرنده', 'line': 'خط', 'report': 'اعتبارسنجی_گزارش', 'language': 'زبان', 'x': 'مختصات_x', 'start': 'اجرا_2', 'rgb': '빛삼원색', 'down': '누르는중', 'listing': 'ارسال_لیست', 'payload': 'داده_های_ضروری_داده_ها', 'proc': 'فرآیند', 'w': '너비값', 'temporary': '임시자원', 'echo': '되돌림서버항목', 'label': 'نام_جدول', 'content': 'محتوا_مقدار', 'argument': '전달값', 'EchoServers': '되돌림서버', 'marker': '확인표시', 'expected': '예상결과', 'test_language': 'test_언어', 'filename': 'فایل_ورودی_نام', 'shell': 'واسط', 'color': '색상', 'transcript': '대화기록', 'offset': 'جابجایی_لایه_ای_مقدار', 'h': '높이값', 'run': 'اجرا_فرمان', 'c': 'کد_نویسه', 'path': 'مسیر', 'encoding': 'مجموعه_نویسه_ها', 'end': 'پایان_دادن_جابجایی_لایه_ای', 'ftp': 'فایل_انتقال_اتصال', 'pixels': '화소들', 'symbol': 'نماد_مقدار', 'source': '원본자료', 'name': 'نام', 'receive': '수신하기', 'manifest': '꾸러미명세'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
