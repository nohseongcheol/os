#!/usr/bin/env python3
"""기존 مسیر 호환 ورودی_نقطه. واقعی_داده_ها 구현: ../ابزارها/예제빌드.py"""
import importlib as 가져오기
import sys as سیستم_عامل_مقدار
from pathlib import Path as مسیر
سیستم_عامل_مقدار.path.insert(0, str(مسیر(__file__).resolve().parents[1] / 'ابزارها'))
if __name__ == '__main__':
    import runpy as برنامه_راه_انداز
    برنامه_راه_انداز.run_module('예제빌드', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('예제빌드')
    대응 = {'out': 'سنجش_داده_ها', 'build_examples': '예제만들기', 'files': 'فایل_لیست', 'java': '자바실행', 'run': 'اجرا_فرمان', 'path': 'مسیر', 'p': 'داده_ها_مرتب_کردن', 'readme': 'مرا_بخوان', 'build_java_library': '자바라이브러리만들기', 'code': '명령열', 'index': 'جستجو_فهرست', 'classes': 'کلاس_مسیر', 'repo': 'مخزن_مسیر', 'root': 'جذر_آدرس', 'content': 'محتوا_مقدار', 'source': '원본자료', 'name': 'نام', 'target': 'هدف', 'manifest': '꾸러미명세', 'language': 'زبان'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
