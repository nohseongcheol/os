#!/usr/bin/env python3
"""기존 مسیر 호환 ورودی_نقطه. واقعی_داده_ها 구현: ../ابزارها/ساخت_کاربر_فضا.py"""
import importlib as 가져오기
import sys as سیستم_عامل_مقدار
from pathlib import Path as مسیر
سیستم_عامل_مقدار.path.insert(0, str(مسیر(__file__).resolve().parents[1] / 'ابزارها'))
if __name__ == '__main__':
    import runpy as برنامه_راه_انداز
    برنامه_راه_انداز.run_module('ساخت_کاربر_فضا', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('ساخت_کاربر_فضا')
    대응 = {'mode': 'روش_حالت', 'header': 'سرصفحه_مقدار', 'i': '순번', 'build_ccompiler': '시언어번역기만들기', 'ar': 'آرشیو_ابزار', 'posix': '포직스경로', 'payload': 'داده_های_ضروری_داده_ها', 'flags': '설정비트', 'cases': '시험사례', 'cc': '시언어번역기', 'data': 'داده_ها', 'build_java_library': '자바라이브러리만들기', 'ld': '연결편집기', 'repo': 'مخزن_مسیر', 'build_python': '파이썬만들기', 'inc': '포함경로', 'argument': '전달값', 'text': 'متن', 'headers': 'سرصفحه_لیست', 'cxx': '시플플번역기', 'valid': '유효함', 'build': 'ساخت', 'build_users': 'ایجاد_کاربر_فضا', 'compiler': '번역기', 'uzlib': '압축해제경로', 'extra': '추가영역', 'phoff': 'برنامه_سرصفحه_جابجایی_لایه_ای', 'offset': 'جابجایی_لایه_ای_مقدار', 'text_address': 'فرمان_آدرس', 'abi': '호출규약', 'assembly': '어셈블리자료', 'run': 'اجرا_فرمان', 'path': 'مسیر', 'p': 'داده_ها_مرتب_کردن', 'changed': '바뀐자료', 'n': '개수', 'flag': 'تنظیمات_مقدار', 'index': 'جستجو_فهرست', 'classes': 'کلاس_مسیر', 'output': '출력결과', 'loads': '적재구획', 'data_address': 'داده_ها_آدرس', 'symbol': 'نماد_مقدار', 'root': 'جذر_آدرس', 'patches': '수정사항', 'source': '원본자료', 'sizes': '크기목록', 'blobs': '탑재덩이들', 'name': 'نام', 'value': 'مقدار', 'fmt': 'قالب_932e03c8', 'work': '작업경로'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
