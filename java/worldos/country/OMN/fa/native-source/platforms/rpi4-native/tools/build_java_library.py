#!/usr/bin/env python3
"""기존 مسیر 호환 ورودی_نقطه. واقعی_داده_ها 구현: ../ابزارها/자바라이브러리빌드.py"""
import importlib as 가져오기
import sys as سیستم_عامل_مقدار
from pathlib import Path as مسیر
سیستم_عامل_مقدار.path.insert(0, str(مسیر(__file__).resolve().parents[1] / 'ابزارها'))
if __name__ == '__main__':
    import runpy as برنامه_راه_انداز
    برنامه_راه_انداز.run_module('자바라이브러리빌드', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('자바라이브러리빌드')
    대응 = {'header': 'سرصفحه_مقدار', 'sources': '원문목록', 'i': '순번', 'info': 'اطلاعات_سیستم', 'payload': 'داده_های_ضروری_داده_ها', 'src': '원본주소', 'run': 'اجرا_فرمان', 'build_java_library': '자바라이브러리만들기', 'relative': '상대경로', 'classes': 'کلاس_مسیر', 'dist': '배포경로', 'archive': 'آرشیو', 'output': '출력결과', 'root': 'جذر_آدرس', 'name': 'نام', 'jar': '자바꾸러미', 'b': '둘째값', 'entries': '항목들'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
