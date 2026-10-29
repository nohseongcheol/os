#!/usr/bin/env python3
"""기존 مسیر 호환 ورودی_نقطه. واقعی_داده_ها 구현: ../ابزارها/시언어번역기빌드.py"""
import importlib as 가져오기
import sys as سیستم_عامل_مقدار
from pathlib import Path as مسیر
سیستم_عامل_مقدار.path.insert(0, str(مسیر(__file__).resolve().parents[1] / 'ابزارها'))
if __name__ == '__main__':
    import runpy as برنامه_راه_انداز
    برنامه_راه_انداز.run_module('시언어번역기빌드', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('시언어번역기빌드')
    대응 = {'out': 'سنجش_داده_ها', 'builtins': '내장연산', 'header': 'سرصفحه_مقدار', 'sdk': '개발꾸러미', 'build_ccompiler': '시언어번역기만들기', 'i': '순번', 'elf': '실행파일', 'run': 'اجرا_فرمان', 'flags': '설정비트', 'path': 'مسیر', 'p': 'داده_ها_مرتب_کردن', 'cc': '시언어번역기', 'obj': 'پرونده_مقصد', 'flag': 'تنظیمات_مقدار', 'ld': '연결편집기', 'objects': 'مقصد_فایل', 'repo': 'مخزن_مسیر', 'v': '임시값', 'upstream': 'بالادست', 'root': 'جذر_آدرس', 'assets': '탑재자료', 'source': '원본자료', 'name': 'نام', 'includes': '포함인수'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
