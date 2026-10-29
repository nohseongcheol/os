#!/usr/bin/env python3
"""기존 راہ 호환 داخلہ_مقام. اصلی_کوائف 구현: ../اوزار/터미널글꼴빌드.py"""
import importlib as 가져오기
import sys as آپریٹنگ_سسٹم_قدر
from pathlib import Path as راہ
آپریٹنگ_سسٹم_قدر.path.insert(0, str(راہ(__file__).resolve().parents[1] / 'اوزار'))
if __name__ == '__main__':
    import runpy as ایپ_عملے_دا_رکن
    ایپ_عملے_دا_رکن.run_module('터미널글꼴빌드', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('터미널글꼴빌드')
    대응 = {'data': 'کوائف', 'img': 'ڈرائنگ_قدر', 'bits': '비트들', 'x': 'x_محدد', 'draw': '화면그리기', 'licences': '이용허락목록', 'paths': 'راہ_فرست', 'y': '세로좌표', 'main': 'چلاؤ', 'src': '원본주소', 'fonts': 'فانٹ_فرست', 'ROOT': '기준', 'p': '자료위치', 'cp': 'کریکٹر_ضابطہ_ربائی', 'target': 'ہدف'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
