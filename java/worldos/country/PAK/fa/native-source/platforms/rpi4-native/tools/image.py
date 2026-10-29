#!/usr/bin/env python3
"""기존 مسیر 호환 ورودی_نقطه. واقعی_داده_ها 구현: ../ابزارها/ایجاد_عکس.py"""
import importlib as 가져오기
import sys as سیستم_عامل_مقدار
from pathlib import Path as مسیر
سیستم_عامل_مقدار.path.insert(0, str(مسیر(__file__).resolve().parents[1] / 'ابزارها'))
if __name__ == '__main__':
    import runpy as برنامه_راه_انداز
    برنامه_راه_انداز.run_module('ایجاد_عکس', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('ایجاد_عکس')
    대응 = {'total': '총량', 'start': 'اجرا_2', 'firmware': '기초제어프로그램', 'files': 'فایل_لیست', 'archive_base': '압축기준', 'partition': 'پارتیشن_فایل', 'archive': 'آرشیو', 'main': 'اجرا_2', 'block': 'داده_ها_مسدود_کردن', 'ROOT': 'نمایش_دادن_جذر', 'boot': '부팅경로', 'stage': 'مرحله_مقدار', 'out': 'سنجش_داده_ها', 'expected': '예상결과', 'f': 'فایل_ورودی', 'src': '원본주소', 'path': 'مسیر', 'p': 'داده_ها_مرتب_کردن', 'extracted': '추출자료', 'member': 'عضو', 'mbr': '주부트기록', 'image': 'عکس', 'sector_count': '섹터개수', 'dist': '배포경로', 'sha': '해시계산', 'license_': 'مجوز', 'source': '원본자료', 'name': 'نام', 'value': 'مقدار', 'manifest': '꾸러미명세', 'dest': 'مقصد_مقدار_مرتب_کردن', 'work': '작업경로'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
