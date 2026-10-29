#!/usr/bin/env python3
"""기존 راستہ_2 호환 اندراج_نقطہ. اصل_کوائف 구현: ../ٹولز/اپ_لوڈ_کريں_فائلیں.py"""
import importlib as 가져오기
import sys as آپریٹنگ_سسٹم_قدر
from pathlib import Path as راستہ_2
آپریٹنگ_سسٹم_قدر.path.insert(0, str(راستہ_2(__file__).resolve().parents[1] / 'ٹولز'))
if __name__ == '__main__':
    import runpy as ایپ_ایپ_دراز
    ایپ_ایپ_دراز.run_module('اپ_لوڈ_کريں_فائلیں', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('اپ_لوڈ_کريں_فائلیں')
    대응 = {'data': 'کوائف', 'i': '순번', 'name': 'نام', 'c': 'کریکٹر_ضابطہ', 'p': 'کوائف_پوزیشن_ٹھیک_کریں', 'args': 'دلائل_لڑی'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
