#!/usr/bin/env python3
"""기존 راههه 호환 داخلا_هنڌ. اصلي_ڪوائف 구현: ../اوزار/부팅시험.py"""
import importlib as 가져오기
import sys as آپريٽنگ_سسٽم_قدر
from pathlib import Path as راههه
آپريٽنگ_سسٽم_قدر.path.insert(0, str(راههه(__file__).resolve().parents[1] / 'اوزار'))
if __name__ == '__main__':
    import runpy as ائپ_ائپ_ڊرائر
    ائپ_ائپ_ڊرائر.run_module('부팅시험', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('부팅시험')
    대응 = {'timeout': '시간제한', 'response': '응답자료', 'msg': 'نيٽ_ورڪ_پيغام', 'exact': '정확한값', 'markers': '확인표시들', 'i': '순번', 'match': '일치', 'execute': 'تعميل_ڪرڻ_ٽاسڪ', 'cancel': 'رد_ڪريو_عمل', 'cmd_byte': 'حڪم_بائٽ', 'reply': 'جواب_ڏيو', 'points': '지점들', 'server': 'سرور_قدر', 'data': 'ڪوائف', 'prompt': 'لقميا', 'enter': 'داخل_ڪريو', 'imported': '들여온파일', 'send': 'اي_ميل', 'main': 'هلائڻ', 'ROOT': '기준', 'text': 'متن', 'first_gui': '첫화면', 'pixel': 'پيل', 'java_class': '자바클래스', 'upload': 'اپ_لوڊ_ڪريو_فائلون', 'pixels_file': 'پيل_فائل', 'pixels_data': 'پيل_ڪوائف', 'edit': 'تدوين_قدر', 'receive_until': '표시까지받기', 'selector': 'چونڊيندڙ', 'size': 'سائيز', 'qmp_path': '모의제어경로', 'key': '누름값', 'second_gui': '둘째화면', 'y': '세로좌표', 'result': '결과', 'samples': '예제들', 'client': 'گراهڪ', 'line': 'لڪير', 'report': 'ڪارگر_رپورٽ', 'work': '작업경로', 'x': 'x_رطبو', 'python_checks': '파이썬검사', 'download': 'ڊائونلوڊ', 'greeting': '인사', 'dims': '치수', 'chunk': '조각', 'deadline': '마감시각', 'proc': 'عمل_a7054519', 'content': 'مواد_قدر', 'block': 'ڪوائف_بلاڪ_ڪريو', 'marker': '확인표시', 'command': 'حڪم', 'expected': '예상결과', 'shell': 'شيل', 'drawing': 'ڊرائنگ_راههه', 'f': 'فائل_داخلا', 'transcript': '대화기록', 'offset': 'آف_سيٽ_قدر', 'path': 'راههه', 'screenshot': 'اسڪرين_جي_ڪلپنگ', 'arguments': '전달인수', 'pixels': '화소들', 'viewer': '화면접속자', 'output': '출력결과', 'stream': 'اسٽريم_قدر', 'cmd': '명령인수', 'name': 'نالو', 'qmp': '모의제어접속'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
