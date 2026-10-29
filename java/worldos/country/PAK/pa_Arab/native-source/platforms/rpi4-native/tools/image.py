#!/usr/bin/env python3
"""기존 راہ 호환 داخلہ_مقام. اصلی_کوائف 구현: ../اوزار/بنڑاؤ_نقش.py"""
import importlib as 가져오기
import sys as آپریٹنگ_سسٹم_قدر
from pathlib import Path as راہ
آپریٹنگ_سسٹم_قدر.path.insert(0, str(راہ(__file__).resolve().parents[1] / 'اوزار'))
if __name__ == '__main__':
    import runpy as ایپ_عملے_دا_رکن
    ایپ_عملے_دا_رکن.run_module('بنڑاؤ_نقش', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('بنڑاؤ_نقش')
    대응 = {'total': '총량', 'start': 'چلاؤ', 'firmware': '기초제어프로그램', 'files': 'فائل_فرست', 'archive_base': '압축기준', 'partition': 'تقسیم_فائل', 'archive': 'محفوظہ', 'main': 'چلاؤ', 'block': 'کوائف_بلاک', 'ROOT': '기준', 'boot': '부팅경로', 'stage': 'مرحلہ_قدر', 'out': '결과자료', 'expected': '예상결과', 'f': 'فائل_داخلہ', 'src': '원본주소', 'path': 'راہ', 'p': '자료위치', 'extracted': '추출자료', 'member': 'رکن', 'mbr': '주부트기록', 'image': 'نقش', 'sector_count': '섹터개수', 'dist': '배포경로', 'sha': '해시계산', 'license_': 'لائسنس', 'source': '원본자료', 'name': 'ناں', 'value': 'قدر', 'manifest': '꾸러미명세', 'dest': '목적위치', 'work': '작업경로'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
