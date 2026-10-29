#!/usr/bin/env python3
"""기존 گوزەر 호환 تێنووسین_خاڵ. ڕاستەکی_دەیتا 구현: ../ئامرازەکان/جێبەجێکردن_فایل.py"""
import importlib as 가져오기
import sys as سیستەمی_کارپێکردن_نرخ
from pathlib import Path as گوزەر
سیستەمی_کارپێکردن_نرخ.path.insert(0, str(گوزەر(__file__).resolve().parents[1] / 'ئامرازەکان'))
if __name__ == '__main__':
    import runpy as بەرنامە_ئەندامی_ستاف
    بەرنامە_ئەندامی_ستاف.run_module('جێبەجێکردن_فایل', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('جێبەجێکردن_فایل')
    대응 = {'timeout': '시간제한', 's': 'رست_دەیتا', 'i': '순번', 'match': '일치', 'files': 'فایل_لیست', 'program': 'بەرنامە', 'executable': '실행가능파일', 'args': 'ئارگیومێنت_ڕیزی_داتا', 'chunk': '조각', 'data': 'دەیتا', 'proc': 'پرۆسە', 'send': 'ناردن', 'main': 'ڕادان', 'marker': '확인표시', 'command': 'فەرمان', 'include': '포함항목', 'dumped': '갈무리자료', 'run': 'جێبەجێکردن_فەرمان', 'p': '자료위치', 'parser': '인수해석기', 'options': 'بەربژارەکان', 'kind': 'پۆل_نرخ', 'selector': 'هەڵبژێرەر', 'upload_data': 'بار_کردن_دەیتا', 'end': 'دوایی_کردن_ئۆفسێت', 'n': '개수', 'd': 'جێمەبەست_دەیتا', 'key': '누름값', 'output': '출력결과', 'line': 'دێڕ', 'name': 'ناو', 'upload_name': 'بار_کردن_ناو', 'receive': '수신하기'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
