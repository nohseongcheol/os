#!/usr/bin/env python3
"""기존 مسیر 호환 ورودی_نقطه. واقعی_داده_ها 구현: ../ابزارها/셸시험.py"""
import importlib as 가져오기
import sys as سیستم_عامل_مقدار
from pathlib import Path as مسیر
سیستم_عامل_مقدار.path.insert(0, str(مسیر(__file__).resolve().parents[1] / 'ابزارها'))
if __name__ == '__main__':
    import runpy as برنامه_راه_انداز
    برنامه_راه_انداز.run_module('셸시험', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('셸시험')
    대응 = {'timeout': '시간제한', 'x': 'مختصات_x', 'msg': 'شبکه_پیام', 'i': '순번', 'reply': 'پاسخ_دادن', 'call': '호출', 'args': 'آرگومان_آرايه', 'chunk': '조각', 'data': 'داده_ها', 'proc': 'فرآیند', 'long_text': '긴글', 'restored': '복원자료', 'send': 'ارسال', 'file': 'پرونده', 'main': 'اجرا_2', 'found': 'جستجو_سنجش', 'ROOT': 'نمایش_دادن_جذر', 'text': 'متن', 'marker': '확인표시', 'command': 'فرمان', 'expected': '예상결과', 'pixel': 'پیکسل', 'shell': 'واسط', 'poll': '준비살피미', 'transcript': '대화기록', 'end': 'پایان_دادن_جابجایی_لایه_ای', 'image': 'عکس', 'key': '누름값', 'y': 'دکمه_Y_مختصات', 'output': '출력결과', 'result': 'سنجش', 'client': 'سرویس_گیرنده', 'line': 'خط', 'stream': 'جریان_مقدار', 'name': 'نام', 'value': 'مقدار', 'receive': '수신하기', 'report': 'اعتبارسنجی_گزارش', 'work': '작업경로', 'qmp': '모의제어접속'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
