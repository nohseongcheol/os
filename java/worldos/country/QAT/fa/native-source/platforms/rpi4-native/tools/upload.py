#!/usr/bin/env python3
"""기존 مسیر 호환 ورودی_نقطه. واقعی_داده_ها 구현: ../ابزارها/آپلود_فایل.py"""
import importlib as 가져오기
import sys as سیستم_عامل_مقدار
from pathlib import Path as مسیر
سیستم_عامل_مقدار.path.insert(0, str(مسیر(__file__).resolve().parents[1] / 'ابزارها'))
if __name__ == '__main__':
    import runpy as برنامه_راه_انداز
    برنامه_راه_انداز.run_module('آپلود_فایل', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('آپلود_فایل')
    대응 = {'data': 'داده_ها', 'i': '순번', 'name': 'نام', 'c': 'کد_نویسه', 'p': 'داده_ها_مرتب_کردن', 'args': 'آرگومان_آرايه'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
