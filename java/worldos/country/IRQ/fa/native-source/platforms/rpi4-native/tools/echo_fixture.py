#!/usr/bin/env python3
"""기존 مسیر 호환 ورودی_نقطه. واقعی_داده_ها 구현: ../ابزارها/되돌림시험서버.py"""
import importlib as 가져오기
import sys as سیستم_عامل_مقدار
from pathlib import Path as مسیر
سیستم_عامل_مقدار.path.insert(0, str(مسیر(__file__).resolve().parents[1] / 'ابزارها'))
if __name__ == '__main__':
    import runpy as برنامه_راه_انداز
    برنامه_راه_انداز.run_module('되돌림시험서버', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('되돌림시험서버')
    대응 = {'data': 'داده_ها', 'e': '보조항목', 'connection': 'اتصال_e05f319b', 'f': 'فایل_ورودی', 'peer': 'مشابه_مقدار', 'self': '자신', 'udp': '전문제어', 't': 'پایانه_ورودی', 'tcp': 'اتصال_کنترل', 'EchoFixture': '되돌림시험서버', 'args': 'آرگومان_آرايه', 'chunk': '조각'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
