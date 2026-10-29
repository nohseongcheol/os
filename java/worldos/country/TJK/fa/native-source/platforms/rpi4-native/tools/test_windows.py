#!/usr/bin/env python3
"""기존 مسیر 호환 ورودی_نقطه. واقعی_داده_ها 구현: ../ابزارها/창시험.py"""
import importlib as 가져오기
import sys as سیستم_عامل_مقدار
from pathlib import Path as مسیر
سیستم_عامل_مقدار.path.insert(0, str(مسیر(__file__).resolve().parents[1] / 'ابزارها'))
if __name__ == '__main__':
    import runpy as برنامه_راه_انداز
    برنامه_راه_انداز.run_module('창시험', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('창시험')
    대응 = {'wait': '기다리기', 'x': 'مختصات_x', 's': 'رشته_داده_ها', 'xy': 'جفت_مختصاتی', 'sel': 'انتخاب_کننده_a916db4e', 'seconds': '초단위', 'log': 'واقعه_نگار_ردیف', 'at': '현재위치', 'send': 'ارسال', 'main': 'اجرا_2', 'req': '요청값', 'hot': 'میانبر_مقدار', 'pump': 'دستگیره_رویداد', 'ROOT': 'نمایش_دادن_جذر', 'marker': '확인표시', 'b': '둘째값', 'command': 'فرمان', 'shell': 'واسط', 'f': 'فایل_ورودی', 'color': '색상', 'click': 'کلیک_دکمه', 'k': '셋째순번', 'c': 'کد_نویسه', 'r': '반환값', 'p': 'داده_ها_مرتب_کردن', 'done': '완료량', 'end': 'پایان_دادن_جابجایی_لایه_ای', 'command_mode': 'فرمان_حالت', 'key': '누름값', 'y': 'دکمه_Y_مختصات', 'pixels': '화소들', 'result': 'سنجش', 'report': 'اعتبارسنجی_گزارش', 'dest': 'مقصد_مقدار_مرتب_کردن', 'work': '작업경로', 'qmp': '모의제어접속'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
