#!/usr/bin/env python3
"""기존 مسیر 호환 ورودی_نقطه. واقعی_داده_ها 구현: ../ابزارها/ساخت_سیستم.py"""
import importlib as 가져오기
import sys as سیستم_عامل_مقدار
from pathlib import Path as مسیر
سیستم_عامل_مقدار.path.insert(0, str(مسیر(__file__).resolve().parents[1] / 'ابزارها'))
if __name__ == '__main__':
    import runpy as برنامه_راه_انداز
    برنامه_راه_انداز.run_module('ساخت_سیستم', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('ساخت_سیستم')
    대응 = {'network': 'شبکه', 'BUILD': 'ساخت_مسیر', 'ar': 'آرشیو_ابزار', 'build_examples': '예제만들기', 'posix': '포직스경로', 'font_data': 'قلم_داده_ها', 'flags': '설정비트', 'a': '첫째값', 'cc': '시언어번역기', 'args': 'آرگومان_آرايه', 'source_flags': '원본설정', 'ld': '연결편집기', 'method': 'روش_ورودی', 'main': 'اجرا_2', 'objcopy': 'شئ_فایل_مبدل', 'ROOT': 'نمایش_دادن_جذر', 'cxx': '시플플번역기', 'includes': '포함인수', 'compiler': '번역기', 'build_users': 'ایجاد_کاربر_فضا', 'f': 'فایل_ورودی', 'extra': '추가영역', 'exports': 'صادرکردن_جدول', 'jobs': '빌드작업', 'run': 'اجرا_فرمان', 'path': 'مسیر', 'REPO': 'مخزن_جذر', 'tool': 'ابزارها', 'classes': 'کلاس_مسیر', 'output': '출력결과', 'samples': '예제들', 'symbol': 'نماد_مقدار', 'source': '원본자료', 'name': 'نام', 'build_network': 'ایجاد_شبکه_48d29d6d', 'font_info': 'قلم_اطلاعات', 'manifest': '꾸러미명세', 'work': '작업경로'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
