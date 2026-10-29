#!/usr/bin/env python3
"""기존 مسیر 호환 ورودی_نقطه. واقعی_داده_ها 구현: ../ابزارها/اجرا_فرمان.py"""
import importlib as 가져오기
import sys as سیستم_عامل_مقدار
from pathlib import Path as مسیر
سیستم_عامل_مقدار.path.insert(0, str(مسیر(__file__).resolve().parents[1] / 'ابزارها'))
if __name__ == '__main__':
    import runpy as برنامه_راه_انداز
    برنامه_راه_انداز.run_module('اجرا_فرمان', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('اجرا_فرمان')
    대응 = {'supported': '지원목록', 'parser': 'مفسر', 'qemu': '모의기계', 'run_desktop': 'اجرا_رایانه', 'main': 'اجرا_2', 'host': 'میزبان', 'status': 'وضعیت_مقدار', 'NetworkBridge': 'شبکه_پل', 'ROOT': 'نمایش_دادن_جذر', 'bridge': 'پل', 'loader': '적재기', 'base': 'زمینه_مقدار_0764f371', 'options': 'گزینه_ها', 'binary': 'دودویی', 'args': 'آرگومان_آرايه', 'command': 'فرمان'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
