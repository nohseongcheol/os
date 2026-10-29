#!/usr/bin/env python3
"""기존 گوزەر 호환 تێنووسین_خاڵ. ڕاستەکی_دەیتا 구현: ../ئامرازەکان/터미널글꼴빌드.py"""
import importlib as 가져오기
import sys as سیستەمی_کارپێکردن_نرخ
from pathlib import Path as گوزەر
سیستەمی_کارپێکردن_نرخ.path.insert(0, str(گوزەر(__file__).resolve().parents[1] / 'ئامرازەکان'))
if __name__ == '__main__':
    import runpy as بەرنامە_ئەندامی_ستاف
    بەرنامە_ئەندامی_ستاف.run_module('터미널글꼴빌드', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('터미널글꼴빌드')
    대응 = {'data': 'دەیتا', 'img': 'نگار_نرخ', 'bits': '비트들', 'x': 'پۆوتانی_x', 'draw': '화면그리기', 'licences': '이용허락목록', 'paths': 'گوزەر_لیست', 'y': '세로좌표', 'main': 'ڕادان', 'src': '원본주소', 'fonts': 'جۆرەپیت_لیست', 'ROOT': '기준', 'p': '자료위치', 'cp': 'نووسە_نهێنبەندی', 'target': 'مەبەست'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
