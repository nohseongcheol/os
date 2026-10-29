#!/usr/bin/env python3
"""기존 مسیر 호환 ورودی_نقطه. واقعی_داده_ها 구현: ../ابزارها/ساخت_شبکه.py"""
import importlib as 가져오기
import sys as سیستم_عامل_مقدار
from pathlib import Path as مسیر
سیستم_عامل_مقدار.path.insert(0, str(مسیر(__file__).resolve().parents[1] / 'ابزارها'))
if __name__ == '__main__':
    import runpy as برنامه_راه_انداز
    برنامه_راه_انداز.run_module('ساخت_شبکه', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('ساخت_شبکه')
    대응 = {'obj': 'پرونده_مقصد', 'objects': 'مقصد_فایل', 'library': 'کتابخانه', 'output': '출력결과', 'port': 'شماره_درگاه', 'root': 'جذر_آدرس', 'files': 'فایل_لیست', 'source': '원본자료', 'run': 'اجرا_فرمان', 'flags': '설정비트', 'path': 'مسیر', 'build_network': 'ایجاد_شبکه_48d29d6d', 'cc': '시언어번역기', 'ar': 'آرشیو_ابزار'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
