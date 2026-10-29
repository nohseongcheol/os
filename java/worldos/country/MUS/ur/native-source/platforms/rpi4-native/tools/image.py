#!/usr/bin/env python3
"""기존 راستہ_2 호환 اندراج_نقطہ. اصل_کوائف 구현: ../ٹولز/بنائیں_نقش.py"""
import importlib as 가져오기
import sys as آپریٹنگ_سسٹم_قدر
from pathlib import Path as راستہ_2
آپریٹنگ_سسٹم_قدر.path.insert(0, str(راستہ_2(__file__).resolve().parents[1] / 'ٹولز'))
if __name__ == '__main__':
    import runpy as ایپ_ایپ_دراز
    ایپ_ایپ_دراز.run_module('بنائیں_نقش', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('بنائیں_نقش')
    대응 = {'total': '총량', 'start': 'چلائیں', 'firmware': '기초제어프로그램', 'files': 'فائل_فہرست', 'archive_base': '압축기준', 'partition': 'بٹوارا_فائل', 'archive': 'محفوظ', 'main': 'چلائیں', 'block': 'کوائف_بلاک_کریں', 'ROOT': 'عکس_ڈالنا_روٹ', 'boot': '부팅경로', 'stage': 'سٹیج_قدر', 'out': 'پیمائش_کوائف', 'expected': '예상결과', 'f': 'فائل_اندراج', 'src': '원본주소', 'path': 'راستہ_2', 'p': 'کوائف_پوزیشن_ٹھیک_کریں', 'extracted': '추출자료', 'member': 'رکن', 'mbr': '주부트기록', 'image': 'نقش', 'sector_count': '섹터개수', 'dist': '배포경로', 'sha': '해시계산', 'license_': 'لائسنس', 'source': '원본자료', 'name': 'نام', 'value': 'قدر', 'manifest': '꾸러미명세', 'dest': 'منزل_مقصود_قدر_پوزیشن_ٹھیک_کریں', 'work': '작업경로'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
