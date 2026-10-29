#!/usr/bin/env python3
"""기존 راستہ_2 호환 اندراج_نقطہ. اصل_کوائف 구현: ../ٹولز/نفاذ_کریں_فائل.py"""
import importlib as 가져오기
import sys as آپریٹنگ_سسٹم_قدر
from pathlib import Path as راستہ_2
آپریٹنگ_سسٹم_قدر.path.insert(0, str(راستہ_2(__file__).resolve().parents[1] / 'ٹولز'))
if __name__ == '__main__':
    import runpy as ایپ_ایپ_دراز
    ایپ_ایپ_دراز.run_module('نفاذ_کریں_فائل', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('نفاذ_کریں_فائل')
    대응 = {'timeout': '시간제한', 's': 'سلک_کوائف', 'i': '순번', 'match': '일치', 'files': 'فائل_فہرست', 'program': 'ایپ', 'executable': '실행가능파일', 'args': 'دلائل_لڑی', 'chunk': '조각', 'data': 'کوائف', 'proc': 'عمل_کاری', 'send': 'بھیجیں', 'main': 'چلائیں', 'marker': '확인표시', 'command': 'حکم', 'include': '포함항목', 'dumped': '갈무리자료', 'run': 'نفاذ_کریں_حکم', 'p': 'کوائف_پوزیشن_ٹھیک_کریں', 'parser': '인수해석기', 'options': 'اختیارات', 'kind': 'زمرہ_قدر', 'selector': 'منتخب_کنندہ', 'upload_data': 'اپ_لوڈ_کريں_کوائف', 'end': 'اختتام_آفسٹ', 'n': '개수', 'd': 'منزل_مقصود_کوائف', 'key': '누름값', 'output': '출력결과', 'line': 'اندراج_کی_سطر', 'name': 'نام', 'upload_name': 'اپ_لوڈ_کريں_نام', 'receive': '수신하기'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
