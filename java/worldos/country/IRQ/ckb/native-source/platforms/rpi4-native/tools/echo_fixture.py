#!/usr/bin/env python3
"""기존 گوزەر 호환 تێنووسین_خاڵ. ڕاستەکی_دەیتا 구현: ../ئامرازەکان/되돌림시험서버.py"""
import importlib as 가져오기
import sys as سیستەمی_کارپێکردن_نرخ
from pathlib import Path as گوزەر
سیستەمی_کارپێکردن_نرخ.path.insert(0, str(گوزەر(__file__).resolve().parents[1] / 'ئامرازەکان'))
if __name__ == '__main__':
    import runpy as بەرنامە_ئەندامی_ستاف
    بەرنامە_ئەندامی_ستاف.run_module('되돌림시험서버', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('되돌림시험서버')
    대응 = {'data': 'دەیتا', 'e': '보조항목', 'connection': 'گرێدان_e05f319b', 'f': 'فایل_تێنووسین', 'peer': 'هاوتا_نرخ', 'self': '자신', 'udp': '전문제어', 't': '터미널항목', 'tcp': 'گرێدان_کۆنترۆڵ', 'EchoFixture': '되돌림시험서버', 'args': 'ئارگیومێنت_ڕیزی_داتا', 'chunk': '조각'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
