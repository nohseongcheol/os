#!/usr/bin/env python3
"""기존 راستہ_2 호환 اندراج_نقطہ. اصل_کوائف 구현: ../ٹولز/بلڈ_ٹرمینل_فانٹ.py"""
import importlib as 가져오기
import sys as آپریٹنگ_سسٹم_قدر
from pathlib import Path as راستہ_2
آپریٹنگ_سسٹم_قدر.path.insert(0, str(راستہ_2(__file__).resolve().parents[1] / 'ٹولز'))
if __name__ == '__main__':
    import runpy as ایپ_ایپ_دراز
    ایپ_ایپ_دراز.run_module('بلڈ_ٹرمینل_فانٹ', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('بلڈ_ٹرمینل_فانٹ')
    대응 = {'data': 'کوائف', 'img': 'ڈرائنگ_قدر', 'bits': '비트들', 'x': 'ایکس_مربوط', 'draw': '화면그리기', 'licences': '이용허락목록', 'paths': 'راہ_فہرست', 'y': '세로좌표', 'main': 'چلائیں', 'src': '원본주소', 'fonts': 'فانٹ_فہرست', 'ROOT': 'عکس_ڈالنا_روٹ', 'p': 'کوائف_پوزیشن_ٹھیک_کریں', 'cp': 'کریکٹر_ضابطہ_بندی', 'target': 'ہدف'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
