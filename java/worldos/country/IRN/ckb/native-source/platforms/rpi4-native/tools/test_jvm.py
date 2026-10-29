#!/usr/bin/env python3
"""기존 گوزەر 호환 تێنووسین_خاڵ. ڕاستەکی_دەیتا 구현: ../ئامرازەکان/자바가상기계시험.py"""
import importlib as 가져오기
import sys as سیستەمی_کارپێکردن_نرخ
from pathlib import Path as گوزەر
سیستەمی_کارپێکردن_نرخ.path.insert(0, str(گوزەر(__file__).resolve().parents[1] / 'ئامرازەکان'))
if __name__ == '__main__':
    import runpy as بەرنامە_ئەندامی_ستاف
    بەرنامە_ئەندامی_ستاف.run_module('자바가상기계시험', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('자바가상기계시험')
    대응 = {'message': '알림문', 's': 'رست_دەیتا', 'actual': '실제결과', 'match': '일치', 'payload': 'بارگەى_كرێ_دەیتا', 'cases': '시험사례', 'fixture': '시험자료', 'main': 'ڕادان', 'ROOT': '기준', 'text': 'دەق', 'valid': '유효함', 'includes': '포함인수', 'include': '포함항목', 'expected': '예상결과', 'sources': '원문목록', 'tmp': '임시경로', 'done': '완료량', 'classes': 'کلاس_گوزەر', 'output': '출력결과', 'result': '결과', 'cmd': '명령인수', 'name': 'ناو', 'jar': '자바꾸러미', 'report': 'ڕەواکردن_ڕاپۆرت', 'tests': '시험목록'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
