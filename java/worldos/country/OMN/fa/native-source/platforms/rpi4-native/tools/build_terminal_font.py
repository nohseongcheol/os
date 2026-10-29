#!/usr/bin/env python3
"""기존 مسیر 호환 ورودی_نقطه. واقعی_داده_ها 구현: ../ابزارها/ساخت_پایانه_قلم.py"""
import importlib as 가져오기
import sys as سیستم_عامل_مقدار
from pathlib import Path as مسیر
سیستم_عامل_مقدار.path.insert(0, str(مسیر(__file__).resolve().parents[1] / 'ابزارها'))
if __name__ == '__main__':
    import runpy as برنامه_راه_انداز
    برنامه_راه_انداز.run_module('ساخت_پایانه_قلم', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('ساخت_پایانه_قلم')
    대응 = {'data': 'داده_ها', 'img': 'نقاشی_مقدار', 'bits': '비트들', 'x': 'مختصات_x', 'draw': '화면그리기', 'licences': '이용허락목록', 'paths': 'مسیر_لیست', 'y': 'دکمه_Y_مختصات', 'main': 'اجرا_2', 'src': '원본주소', 'fonts': 'قلم_لیست', 'ROOT': 'نمایش_دادن_جذر', 'p': 'داده_ها_مرتب_کردن', 'cp': 'نویسه_رمزگذاری', 'target': 'هدف'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
