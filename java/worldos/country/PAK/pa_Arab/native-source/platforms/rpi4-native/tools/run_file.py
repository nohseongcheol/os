#!/usr/bin/env python3
"""기존 راہ 호환 داخلہ_مقام. اصلی_کوائف 구현: ../اوزار/نفاذ_کرو_فائل.py"""
import importlib as 가져오기
import sys as آپریٹنگ_سسٹم_قدر
from pathlib import Path as راہ
آپریٹنگ_سسٹم_قدر.path.insert(0, str(راہ(__file__).resolve().parents[1] / 'اوزار'))
if __name__ == '__main__':
    import runpy as ایپ_عملے_دا_رکن
    ایپ_عملے_دا_رکن.run_module('نفاذ_کرو_فائل', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('نفاذ_کرو_فائل')
    대응 = {'timeout': '시간제한', 's': 'سٹرنگ_کوائف', 'i': '순번', 'match': '일치', 'files': 'فائل_فرست', 'program': 'ایپ', 'executable': '실행가능파일', 'args': 'دلیل_ایرے', 'chunk': '조각', 'data': 'کوائف', 'proc': 'عمل', 'send': 'بھیجو', 'main': 'چلاؤ', 'marker': '확인표시', 'command': 'حکم', 'include': '포함항목', 'dumped': '갈무리자료', 'run': 'نفاذ_کرو_حکم', 'p': '자료위치', 'parser': '인수해석기', 'options': 'اختیار', 'kind': 'زمرہ_قدر', 'selector': 'منتخب_کرنڑ_آلا', 'upload_data': 'اپ_لوڈ_کرو_کوائف', 'end': 'ختم_کرو_آف_سیٹ', 'n': '개수', 'd': 'منزل_مقصود_کوائف', 'key': '누름값', 'output': '출력결과', 'line': 'لائن', 'name': 'ناں', 'upload_name': 'اپ_لوڈ_کرو_ناں', 'receive': '수신하기'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
