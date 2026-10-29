#!/usr/bin/env python3
"""기존 راستہ_2 호환 اندراج_نقطہ. اصل_کوائف 구현: ../ٹولز/원격한글시험.py"""
import importlib as 가져오기
import sys as آپریٹنگ_سسٹم_قدر
from pathlib import Path as راستہ_2
آپریٹنگ_سسٹم_قدر.path.insert(0, str(راستہ_2(__file__).resolve().parents[1] / 'ٹولز'))
if __name__ == '__main__':
    import runpy as ایپ_ایپ_دراز
    ایپ_ایپ_دراز.run_module('원격한글시험', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('원격한글시험')
    대응 = {'wait': '기다리기', 'typing': '글자입력', 'start': 'چلائیں', 'profile': 'پروفائل', 'focused': 'مرکوز', 'serial': '직렬입출력', 'keys': '누름열', 'server': 'سرور_قدر', 'log': 'لاگ_صف', 'args': 'دلائل_لڑی', 'deadline': '마감시각', 'data': 'کوائف', 'candidate': '후보', 'logs': '기록들', 'kw': '이름붙인인수', 'number': '수치', 'main': 'چلائیں', 'ready': '준비완료', 'found': 'تلاش_پیمائش', 'guest': 'مہمان', 'ROOT': 'عکس_ڈالنا_روٹ', 'marker': '확인표시', 'text': 'متن', 'out': 'پیمائش_کوائف', 'env': '환경', 'f': 'فائل_اندراج', 'port': 'دہانہ_نمبر', 'offset': 'آفسٹ_قدر', 'version': '판번호', 'p': 'کوائف_پوزیشن_ٹھیک_کریں', 'selector': 'منتخب_کنندہ', 'xvfb': 'مجازی_ڈسپلے', 'display': 'ڈسپلے', 'n': '개수', 'key': '누름값', 'processes': '실행과정들', 'rootfs': '뿌리파일계층', 'xdo': '가상입력도구', 'name': 'نام', 'window': 'ونڈو', 'report': 'توثیق_رپورٹ', 'work': '작업경로'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
