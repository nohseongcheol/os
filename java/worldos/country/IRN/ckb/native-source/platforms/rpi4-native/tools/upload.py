#!/usr/bin/env python3
"""기존 گوزەر 호환 تێنووسین_خاڵ. ڕاستەکی_دەیتا 구현: ../ئامرازەکان/بار_کردن_فایله_کان.py"""
import importlib as 가져오기
import sys as سیستەمی_کارپێکردن_نرخ
from pathlib import Path as گوزەر
سیستەمی_کارپێکردن_نرخ.path.insert(0, str(گوزەر(__file__).resolve().parents[1] / 'ئامرازەکان'))
if __name__ == '__main__':
    import runpy as بەرنامە_ئەندامی_ستاف
    بەرنامە_ئەندامی_ستاف.run_module('بار_کردن_فایله_کان', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('بار_کردن_فایله_کان')
    대응 = {'data': 'دەیتا', 'i': '순번', 'name': 'ناو', 'c': 'کۆدی_نووسە', 'p': '자료위치', 'args': 'ئارگیومێنت_ڕیزی_داتا'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
