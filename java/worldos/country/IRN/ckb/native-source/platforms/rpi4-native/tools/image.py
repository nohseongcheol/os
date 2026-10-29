#!/usr/bin/env python3
"""기존 گوزەر 호환 تێنووسین_خاڵ. ڕاستەکی_دەیتا 구현: ../ئامرازەکان/دروستکردن_وێنە.py"""
import importlib as 가져오기
import sys as سیستەمی_کارپێکردن_نرخ
from pathlib import Path as گوزەر
سیستەمی_کارپێکردن_نرخ.path.insert(0, str(گوزەر(__file__).resolve().parents[1] / 'ئامرازەکان'))
if __name__ == '__main__':
    import runpy as بەرنامە_ئەندامی_ستاف
    بەرنامە_ئەندامی_ستاف.run_module('دروستکردن_وێنە', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('دروستکردن_وێنە')
    대응 = {'total': '총량', 'start': 'ڕادان', 'firmware': '기초제어프로그램', 'files': 'فایل_لیست', 'archive_base': '압축기준', 'partition': 'پارچەبەند_فایل', 'archive': 'ئەرشیف', 'main': 'ڕادان', 'block': 'دەیتا_بلۆک_کردن', 'ROOT': '기준', 'boot': '부팅경로', 'stage': 'قۆناغ_نرخ', 'out': '결과자료', 'expected': '예상결과', 'f': 'فایل_تێنووسین', 'src': '원본주소', 'path': 'گوزەر', 'p': '자료위치', 'extracted': '추출자료', 'member': 'ئەندام', 'mbr': '주부트기록', 'image': 'وێنە', 'sector_count': '섹터개수', 'dist': '배포경로', 'sha': '해시계산', 'license_': 'پەرمان', 'source': '원본자료', 'name': 'ناو', 'value': 'نرخ', 'manifest': '꾸러미명세', 'dest': '목적위치', 'work': '작업경로'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
