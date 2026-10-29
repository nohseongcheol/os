#!/usr/bin/env python3
"""기존 مسیر 호환 ورودی_نقطه. واقعی_داده_ها 구현: ../ابزارها/자바가상기계시험.py"""
import importlib as 가져오기
import sys as سیستم_عامل_مقدار
from pathlib import Path as مسیر
سیستم_عامل_مقدار.path.insert(0, str(مسیر(__file__).resolve().parents[1] / 'ابزارها'))
if __name__ == '__main__':
    import runpy as برنامه_راه_انداز
    برنامه_راه_انداز.run_module('자바가상기계시험', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('자바가상기계시험')
    대응 = {'message': '알림문', 's': 'رشته_داده_ها', 'actual': 'واقعی_سنجش', 'match': '일치', 'payload': 'داده_های_ضروری_داده_ها', 'cases': '시험사례', 'fixture': '시험자료', 'main': 'اجرا_2', 'ROOT': 'نمایش_دادن_جذر', 'text': 'متن', 'valid': '유효함', 'includes': '포함인수', 'include': '포함항목', 'expected': '예상결과', 'sources': '원문목록', 'tmp': '임시경로', 'done': '완료량', 'classes': 'کلاس_مسیر', 'output': '출력결과', 'result': 'سنجش', 'cmd': '명령인수', 'name': 'نام', 'jar': '자바꾸러미', 'report': 'اعتبارسنجی_گزارش', 'tests': '시험목록'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
