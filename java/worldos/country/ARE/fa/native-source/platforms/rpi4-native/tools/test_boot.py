#!/usr/bin/env python3
"""기존 مسیر 호환 ورودی_نقطه. واقعی_داده_ها 구현: ../ابزارها/부팅시험.py"""
import importlib as 가져오기
import sys as سیستم_عامل_مقدار
from pathlib import Path as مسیر
سیستم_عامل_مقدار.path.insert(0, str(مسیر(__file__).resolve().parents[1] / 'ابزارها'))
if __name__ == '__main__':
    import runpy as برنامه_راه_انداز
    برنامه_راه_انداز.run_module('부팅시험', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('부팅시험')
    대응 = {'timeout': '시간제한', 'response': '응답자료', 'msg': 'شبکه_پیام', 'exact': '정확한값', 'markers': '확인표시들', 'i': '순번', 'match': '일치', 'execute': 'اجرا', 'cancel': 'لغو_عملیات', 'cmd_byte': 'فرمان_بایت', 'reply': 'پاسخ_دادن', 'points': '지점들', 'server': 'سرور_مقدار', 'data': 'داده_ها', 'prompt': 'فرمان_1dd14da4', 'enter': 'وارد_کردن', 'imported': '들여온파일', 'send': 'ارسال', 'main': 'اجرا_2', 'ROOT': 'نمایش_دادن_جذر', 'text': 'متن', 'first_gui': '첫화면', 'pixel': 'پیکسل', 'java_class': '자바클래스', 'upload': 'آپلود_فایل', 'pixels_file': 'پیکسل_فایل', 'pixels_data': 'پیکسل_داده_ها', 'edit': 'ویرایش_مقدار', 'receive_until': '표시까지받기', 'selector': 'انتخاب_کننده', 'size': 'اندازه', 'qmp_path': '모의제어경로', 'key': '누름값', 'second_gui': '둘째화면', 'y': 'دکمه_Y_مختصات', 'result': 'سنجش', 'samples': '예제들', 'client': 'سرویس_گیرنده', 'line': 'خط', 'report': 'اعتبارسنجی_گزارش', 'work': '작업경로', 'x': 'مختصات_x', 'python_checks': '파이썬검사', 'download': 'دانلود', 'greeting': '인사', 'dims': '치수', 'chunk': '조각', 'deadline': '마감시각', 'proc': 'فرآیند', 'content': 'محتوا_مقدار', 'block': 'داده_ها_مسدود_کردن', 'marker': '확인표시', 'command': 'فرمان', 'expected': '예상결과', 'shell': 'واسط', 'drawing': 'نقاشی_مسیر', 'f': 'فایل_ورودی', 'transcript': '대화기록', 'offset': 'جابجایی_لایه_ای_مقدار', 'path': 'مسیر', 'screenshot': 'برش_صفحه', 'arguments': '전달인수', 'pixels': '화소들', 'viewer': '화면접속자', 'output': '출력결과', 'stream': 'جریان_مقدار', 'cmd': '명령인수', 'name': 'نام', 'qmp': '모의제어접속'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
