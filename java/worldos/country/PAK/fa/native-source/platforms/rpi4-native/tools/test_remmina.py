#!/usr/bin/env python3
"""기존 مسیر 호환 ورودی_نقطه. واقعی_داده_ها 구현: ../ابزارها/원격한글시험.py"""
import importlib as 가져오기
import sys as سیستم_عامل_مقدار
from pathlib import Path as مسیر
سیستم_عامل_مقدار.path.insert(0, str(مسیر(__file__).resolve().parents[1] / 'ابزارها'))
if __name__ == '__main__':
    import runpy as برنامه_راه_انداز
    برنامه_راه_انداز.run_module('원격한글시험', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('원격한글시험')
    대응 = {'wait': '기다리기', 'typing': '글자입력', 'start': 'اجرا_2', 'profile': 'نمایه', 'focused': 'متمرکز', 'serial': '직렬입출력', 'keys': '누름열', 'server': 'سرور_مقدار', 'log': 'واقعه_نگار_ردیف', 'args': 'آرگومان_آرايه', 'deadline': '마감시각', 'data': 'داده_ها', 'candidate': '후보', 'logs': '기록들', 'kw': '이름붙인인수', 'number': '수치', 'main': 'اجرا_2', 'ready': '준비완료', 'found': 'جستجو_سنجش', 'guest': 'مهمان', 'ROOT': 'نمایش_دادن_جذر', 'marker': '확인표시', 'text': 'متن', 'out': 'سنجش_داده_ها', 'env': '환경', 'f': 'فایل_ورودی', 'port': 'شماره_درگاه', 'offset': 'جابجایی_لایه_ای_مقدار', 'version': '판번호', 'p': 'داده_ها_مرتب_کردن', 'selector': 'انتخاب_کننده', 'xvfb': 'مجازی_صفحه_نمایش', 'display': 'صفحه_نمایش', 'n': '개수', 'key': '누름값', 'processes': '실행과정들', 'rootfs': '뿌리파일계층', 'xdo': '가상입력도구', 'name': 'نام', 'window': 'پنجره', 'report': 'اعتبارسنجی_گزارش', 'work': '작업경로'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
