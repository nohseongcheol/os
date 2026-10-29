#!/usr/bin/env python3
"""기존 راہ 호환 داخلہ_مقام. اصلی_کوائف 구현: ../اوزار/부팅시험.py"""
import importlib as 가져오기
import sys as آپریٹنگ_سسٹم_قدر
from pathlib import Path as راہ
آپریٹنگ_سسٹم_قدر.path.insert(0, str(راہ(__file__).resolve().parents[1] / 'اوزار'))
if __name__ == '__main__':
    import runpy as ایپ_عملے_دا_رکن
    ایپ_عملے_دا_رکن.run_module('부팅시험', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('부팅시험')
    대응 = {'timeout': '시간제한', 'response': '응답자료', 'msg': 'نیٹ_ورک_پیغام', 'exact': '정확한값', 'markers': '확인표시들', 'i': '순번', 'match': '일치', 'execute': 'نفاذ_کرو_ٹاسک', 'cancel': 'منسوخ_کرو_عمل', 'cmd_byte': 'حکم_بائٹ', 'reply': 'جواب_دیوؤ', 'points': '지점들', 'server': 'سرور_قدر', 'data': 'کوائف', 'prompt': 'لقمیا', 'enter': 'داخل_کرو', 'imported': '들여온파일', 'send': 'بھیجو', 'main': 'چلاؤ', 'ROOT': '기준', 'text': 'متن', 'first_gui': '첫화면', 'pixel': 'دانہ', 'java_class': '자바클래스', 'upload': 'اپ_لوڈ_کرو_فائلاں', 'pixels_file': 'دانہ_فائل', 'pixels_data': 'دانہ_کوائف', 'edit': 'تدوین_قدر', 'receive_until': '표시까지받기', 'selector': 'منتخب_کرنڑ_آلا', 'size': 'سائز', 'qmp_path': '모의제어경로', 'key': '누름값', 'second_gui': '둘째화면', 'y': '세로좌표', 'result': '결과', 'samples': '예제들', 'client': 'گاہک', 'line': 'لائن', 'report': 'جواز_دہی_رپورٹ', 'work': '작업경로', 'x': 'x_محدد', 'python_checks': '파이썬검사', 'download': 'ڈاؤن_لوڈ', 'greeting': '인사', 'dims': '치수', 'chunk': '조각', 'deadline': '마감시각', 'proc': 'عمل', 'content': 'اجزاء_قدر', 'block': 'کوائف_بلاک', 'marker': '확인표시', 'command': 'حکم', 'expected': '예상결과', 'shell': 'شیل', 'drawing': 'ڈرائنگ_راہ', 'f': 'فائل_داخلہ', 'transcript': '대화기록', 'offset': 'آف_سیٹ_قدر', 'path': 'راہ', 'screenshot': 'سکرین_دی_ویڈیو', 'arguments': '전달인수', 'pixels': '화소들', 'viewer': '화면접속자', 'output': '출력결과', 'stream': 'سٹریم_قدر', 'cmd': '명령인수', 'name': 'ناں', 'qmp': '모의제어접속'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
