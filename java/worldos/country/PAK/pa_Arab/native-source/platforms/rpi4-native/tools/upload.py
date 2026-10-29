#!/usr/bin/env python3
"""기존 راہ 호환 داخلہ_مقام. اصلی_کوائف 구현: ../اوزار/اپ_لوڈ_کرو_فائلاں.py"""
import importlib as 가져오기
import sys as آپریٹنگ_سسٹم_قدر
from pathlib import Path as راہ
آپریٹنگ_سسٹم_قدر.path.insert(0, str(راہ(__file__).resolve().parents[1] / 'اوزار'))
if __name__ == '__main__':
    import runpy as ایپ_عملے_دا_رکن
    ایپ_عملے_دا_رکن.run_module('اپ_لوڈ_کرو_فائلاں', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('اپ_لوڈ_کرو_فائلاں')
    대응 = {'data': 'کوائف', 'i': '순번', 'name': 'ناں', 'c': 'کیریکٹر_کوڈ', 'p': '자료위치', 'args': 'دلیل_ایرے'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
