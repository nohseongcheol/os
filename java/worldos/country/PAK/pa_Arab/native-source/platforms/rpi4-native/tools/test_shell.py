#!/usr/bin/env python3
"""기존 راہ 호환 داخلہ_مقام. اصلی_کوائف 구현: ../اوزار/셸시험.py"""
import importlib as 가져오기
import sys as آپریٹنگ_سسٹم_قدر
from pathlib import Path as راہ
آپریٹنگ_سسٹم_قدر.path.insert(0, str(راہ(__file__).resolve().parents[1] / 'اوزار'))
if __name__ == '__main__':
    import runpy as ایپ_عملے_دا_رکن
    ایپ_عملے_دا_رکن.run_module('셸시험', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('셸시험')
    대응 = {'timeout': '시간제한', 'x': 'x_محدد', 'msg': 'نیٹ_ورک_پیغام', 'i': '순번', 'reply': 'جواب_دیوؤ', 'call': '호출', 'args': 'دلیل_ایرے', 'chunk': '조각', 'data': 'کوائف', 'proc': 'عمل', 'long_text': '긴글', 'restored': '복원자료', 'send': 'بھیجو', 'file': 'فائل', 'main': 'چلاؤ', 'found': '찾은결과', 'ROOT': '기준', 'text': 'متن', 'marker': '확인표시', 'command': 'حکم', 'expected': '예상결과', 'pixel': 'دانہ', 'shell': 'شیل', 'poll': '준비살피미', 'transcript': '대화기록', 'end': 'ختم_کرو_آف_سیٹ', 'image': 'نقش', 'key': '누름값', 'y': '세로좌표', 'output': '출력결과', 'result': '결과', 'client': 'گاہک', 'line': 'لائن', 'stream': 'سٹریم_قدر', 'name': 'ناں', 'value': 'قدر', 'receive': '수신하기', 'report': 'جواز_دہی_رپورٹ', 'work': '작업경로', 'qmp': '모의제어접속'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
