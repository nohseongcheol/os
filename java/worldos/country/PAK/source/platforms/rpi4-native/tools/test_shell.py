#!/usr/bin/env python3
"""기존 راستہ_2 호환 اندراج_نقطہ. اصل_کوائف 구현: ../ٹولز/셸시험.py"""
import importlib as 가져오기
import sys as آپریٹنگ_سسٹم_قدر
from pathlib import Path as راستہ_2
آپریٹنگ_سسٹم_قدر.path.insert(0, str(راستہ_2(__file__).resolve().parents[1] / 'ٹولز'))
if __name__ == '__main__':
    import runpy as ایپ_ایپ_دراز
    ایپ_ایپ_دراز.run_module('셸시험', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('셸시험')
    대응 = {'timeout': '시간제한', 'x': 'ایکس_مربوط', 'msg': 'نیٹ_ورک_پیغام', 'i': '순번', 'reply': 'جواب_دیں', 'call': '호출', 'args': 'دلائل_لڑی', 'chunk': '조각', 'data': 'کوائف', 'proc': 'عمل_کاری', 'long_text': '긴글', 'restored': '복원자료', 'send': 'بھیجیں', 'file': 'فائل_کا_نام', 'main': 'چلائیں', 'found': 'تلاش_پیمائش', 'ROOT': 'عکس_ڈالنا_روٹ', 'text': 'متن', 'marker': '확인표시', 'command': 'حکم', 'expected': '예상결과', 'pixel': 'پکسل', 'shell': 'شیل', 'poll': '준비살피미', 'transcript': '대화기록', 'end': 'اختتام_آفسٹ', 'image': 'نقش', 'key': '누름값', 'y': '세로좌표', 'output': '출력결과', 'result': 'پیمائش', 'client': 'کلائنٹ', 'line': 'اندراج_کی_سطر', 'stream': 'بہاؤ_قدر', 'name': 'نام', 'value': 'قدر', 'receive': '수신하기', 'report': 'توثیق_رپورٹ', 'work': '작업경로', 'qmp': '모의제어접속'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
