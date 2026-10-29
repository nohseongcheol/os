#!/usr/bin/env python3
"""기존 راہ 호환 داخلہ_مقام. اصلی_کوائف 구현: ../اوزار/되돌림시험서버.py"""
import importlib as 가져오기
import sys as آپریٹنگ_سسٹم_قدر
from pathlib import Path as راہ
آپریٹنگ_سسٹم_قدر.path.insert(0, str(راہ(__file__).resolve().parents[1] / 'اوزار'))
if __name__ == '__main__':
    import runpy as ایپ_عملے_دا_رکن
    ایپ_عملے_دا_رکن.run_module('되돌림시험서버', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('되돌림시험서버')
    대응 = {'data': 'کوائف', 'e': '보조항목', 'connection': 'کنکشن_e05f319b', 'f': 'فائل_داخلہ', 'peer': 'ہم_سر_قدر', 'self': '자신', 'udp': '전문제어', 't': '터미널항목', 'tcp': 'کنکشن_کنٹرول', 'EchoFixture': '되돌림시험서버', 'args': 'دلیل_ایرے', 'chunk': '조각'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
