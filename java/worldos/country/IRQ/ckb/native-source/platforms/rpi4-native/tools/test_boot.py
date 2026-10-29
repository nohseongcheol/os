#!/usr/bin/env python3
"""기존 گوزەر 호환 تێنووسین_خاڵ. ڕاستەکی_دەیتا 구현: ../ئامرازەکان/부팅시험.py"""
import importlib as 가져오기
import sys as سیستەمی_کارپێکردن_نرخ
from pathlib import Path as گوزەر
سیستەمی_کارپێکردن_نرخ.path.insert(0, str(گوزەر(__file__).resolve().parents[1] / 'ئامرازەکان'))
if __name__ == '__main__':
    import runpy as بەرنامە_ئەندامی_ستاف
    بەرنامە_ئەندامی_ستاف.run_module('부팅시험', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('부팅시험')
    대응 = {'timeout': '시간제한', 'response': '응답자료', 'msg': 'تۆڕ_پەیام', 'exact': '정확한값', 'markers': '확인표시들', 'i': '순번', 'match': '일치', 'execute': 'جێبەجێکردن_ئەرک', 'cancel': 'بەتاڵ_کردنەوە_کار', 'cmd_byte': 'فەرمان_بایت', 'reply': 'وەڵامدانەوه', 'points': '지점들', 'server': 'ڕاژەکار_نرخ', 'data': 'دەیتا', 'prompt': 'برووسکە', 'enter': 'تێنووسین', 'imported': '들여온파일', 'send': 'ناردن', 'main': 'ڕادان', 'ROOT': '기준', 'text': 'دەق', 'first_gui': '첫화면', 'pixel': 'پێڵ', 'java_class': '자바클래스', 'upload': 'بار_کردن_فایله_کان', 'pixels_file': 'پێڵ_فایل', 'pixels_data': 'پێڵ_دەیتا', 'edit': 'بژار_نرخ', 'receive_until': '표시까지받기', 'selector': 'هەڵبژێرەر', 'size': 'گۆڕینی_ئەندازە', 'qmp_path': '모의제어경로', 'key': '누름값', 'second_gui': '둘째화면', 'y': '세로좌표', 'result': '결과', 'samples': '예제들', 'client': 'کلایەنت', 'line': 'دێڕ', 'report': 'ڕەواکردن_ڕاپۆرت', 'work': '작업경로', 'x': 'پۆوتانی_x', 'python_checks': '파이썬검사', 'download': 'داگرتن', 'greeting': '인사', 'dims': '치수', 'chunk': '조각', 'deadline': '마감시각', 'proc': 'پرۆسە', 'content': 'ناوەرۆک_نرخ', 'block': 'دەیتا_بلۆک_کردن', 'marker': '확인표시', 'command': 'فەرمان', 'expected': '예상결과', 'shell': 'توێکڵ', 'drawing': 'نگار_گوزەر', 'f': 'فایل_تێنووسین', 'transcript': '대화기록', 'offset': 'ئۆفسێت_نرخ', 'path': 'گوزەر', 'screenshot': 'وێنەی_شاشە', 'arguments': '전달인수', 'pixels': '화소들', 'viewer': '화면접속자', 'output': '출력결과', 'stream': 'Stream_نرخ', 'cmd': '명령인수', 'name': 'ناو', 'qmp': '모의제어접속'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
