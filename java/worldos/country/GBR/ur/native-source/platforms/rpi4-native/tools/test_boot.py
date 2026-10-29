#!/usr/bin/env python3
"""기존 راستہ_2 호환 اندراج_نقطہ. اصل_کوائف 구현: ../ٹولز/부팅시험.py"""
import importlib as 가져오기
import sys as آپریٹنگ_سسٹم_قدر
from pathlib import Path as راستہ_2
آپریٹنگ_سسٹم_قدر.path.insert(0, str(راستہ_2(__file__).resolve().parents[1] / 'ٹولز'))
if __name__ == '__main__':
    import runpy as ایپ_ایپ_دراز
    ایپ_ایپ_دراز.run_module('부팅시험', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('부팅시험')
    대응 = {'timeout': '시간제한', 'response': '응답자료', 'msg': 'نیٹ_ورک_پیغام', 'exact': '정확한값', 'markers': '확인표시들', 'i': '순번', 'match': '일치', 'execute': 'اطلاق', 'cancel': 'منسوخ_عملیہ', 'cmd_byte': 'حکم_بائٹ', 'reply': 'جواب_دیں', 'points': '지점들', 'server': 'سرور_قدر', 'data': 'کوائف', 'prompt': 'فوری', 'enter': 'داخل_کریں', 'imported': '들여온파일', 'send': 'بھیجیں', 'main': 'چلائیں', 'ROOT': 'عکس_ڈالنا_روٹ', 'text': 'متن', 'first_gui': '첫화면', 'pixel': 'پکسل', 'java_class': '자바클래스', 'upload': 'اپ_لوڈ_کريں_فائلیں', 'pixels_file': 'پکسل_فائل', 'pixels_data': 'پکسل_کوائف', 'edit': 'تدوین_قدر', 'receive_until': '표시까지받기', 'selector': 'منتخب_کنندہ', 'size': 'حجم', 'qmp_path': '모의제어경로', 'key': '누름값', 'second_gui': '둘째화면', 'y': '세로좌표', 'result': 'پیمائش', 'samples': '예제들', 'client': 'کلائنٹ', 'line': 'اندراج_کی_سطر', 'report': 'توثیق_رپورٹ', 'work': '작업경로', 'x': 'ایکس_مربوط', 'python_checks': '파이썬검사', 'download': 'ڈاؤن_لوڈ', 'greeting': '인사', 'dims': '치수', 'chunk': '조각', 'deadline': '마감시각', 'proc': 'عمل_کاری', 'content': 'مشمول_قدر', 'block': 'کوائف_بلاک_کریں', 'marker': '확인표시', 'command': 'حکم', 'expected': '예상결과', 'shell': 'شیل', 'drawing': 'ڈرائنگ_راہ', 'f': 'فائل_اندراج', 'transcript': '대화기록', 'offset': 'آفسٹ_قدر', 'path': 'راستہ_2', 'screenshot': 'سکرين_تراشے', 'arguments': '전달인수', 'pixels': '화소들', 'viewer': '화면접속자', 'output': '출력결과', 'stream': 'بہاؤ_قدر', 'cmd': '명령인수', 'name': 'نام', 'qmp': '모의제어접속'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
