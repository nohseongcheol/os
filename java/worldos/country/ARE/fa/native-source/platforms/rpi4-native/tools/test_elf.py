#!/usr/bin/env python3
"""기존 مسیر 호환 ورودی_نقطه. واقعی_داده_ها 구현: ../ابزارها/실행파일시험.py"""
import importlib as 가져오기
import sys as سیستم_عامل_مقدار
from pathlib import Path as مسیر
سیستم_عامل_مقدار.path.insert(0, str(مسیر(__file__).resolve().parents[1] / 'ابزارها'))
if __name__ == '__main__':
    import runpy as برنامه_راه_انداز
    برنامه_راه_انداز.run_module('실행파일시험', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('실행파일시험')
    대응 = {'out': 'سنجش_داده_ها', 'expected': '예상결과', 'phoff': 'برنامه_سرصفحه_جابجایی_لایه_ای', 'offset': 'جابجایی_لایه_ای_مقدار', 'invalid': 'بی_اعتبار_داده_ها', 'path': 'مسیر', 'executable': '실행가능파일', 'rejected': '거부결과', 'linux_example': '리눅스예제', 'original': '원본', 'result': 'سنجش', 'format_': 'قالب_b87fd068', 'main': 'اجرا_2', 'content': 'محتوا_مقدار', 'source': '원본자료', 'name': 'نام', 'reference': 'مقایسه_پایه', 'ROOT': 'نمایش_دادن_جذر', 'value': 'مقدار', 'report': 'اعتبارسنجی_گزارش'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
