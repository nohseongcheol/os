#!/usr/bin/env python3
"""기존 راہ 호환 داخلہ_مقام. اصلی_کوائف 구현: ../اوزار/자바가상기계시험.py"""
import importlib as 가져오기
import sys as آپریٹنگ_سسٹم_قدر
from pathlib import Path as راہ
آپریٹنگ_سسٹم_قدر.path.insert(0, str(راہ(__file__).resolve().parents[1] / 'اوزار'))
if __name__ == '__main__':
    import runpy as ایپ_عملے_دا_رکن
    ایپ_عملے_دا_رکن.run_module('자바가상기계시험', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('자바가상기계시험')
    대응 = {'message': '알림문', 's': 'سٹرنگ_کوائف', 'actual': '실제결과', 'match': '일치', 'payload': 'پے_لوڈ_کوائف', 'cases': '시험사례', 'fixture': '시험자료', 'main': 'چلاؤ', 'ROOT': '기준', 'text': 'متن', 'valid': '유효함', 'includes': '포함인수', 'include': '포함항목', 'expected': '예상결과', 'sources': '원문목록', 'tmp': '임시경로', 'done': '완료량', 'classes': 'درجہ_راہ', 'output': '출력결과', 'result': '결과', 'cmd': '명령인수', 'name': 'ناں', 'jar': '자바꾸러미', 'report': 'جواز_دہی_رپورٹ', 'tests': '시험목록'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
