#!/usr/bin/env python3
"""기존 راستہ_2 호환 اندراج_نقطہ. اصل_کوائف 구현: ../ٹولز/되돌림시험서버.py"""
import importlib as 가져오기
import sys as آپریٹنگ_سسٹم_قدر
from pathlib import Path as راستہ_2
آپریٹنگ_سسٹم_قدر.path.insert(0, str(راستہ_2(__file__).resolve().parents[1] / 'ٹولز'))
if __name__ == '__main__':
    import runpy as ایپ_ایپ_دراز
    ایپ_ایپ_دراز.run_module('되돌림시험서버', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('되돌림시험서버')
    대응 = {'data': 'کوائف', 'e': '보조항목', 'connection': 'رابطہ_e05f319b', 'f': 'فائل_اندراج', 'peer': 'ساتھی_قدر', 'self': '자신', 'udp': '전문제어', 't': 'ٹرمینل_اندراج', 'tcp': 'رابطہ_کنٹرول', 'EchoFixture': '되돌림시험서버', 'args': 'دلائل_لڑی', 'chunk': '조각'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
