#!/usr/bin/env python3
"""기존 path 호환 pagpasok_point. totoo_data 구현: ../Mga_Tool/한글입력시험.py"""
import importlib as TAKE_VALUE
import sys as operating_system_VALUE
from pathlib import Path as path
operating_system_VALUE.path.insert(0, str(path(__file__).resolve().parents[1] / 'Mga_Tool'))
if __name__ == '__main__':
    import runpy as app_launcher
    app_launcher.run_module('한글입력시험', run_name='__main__', alter_sys=True)
else:
    구현 = TAKE_VALUE.import_module('한글입력시험')
    대응 = {'expected': '예상결과', 'Keyboard': 'keyboard', 'press': '글쇠누르기', 'self': '자신', 'test_modes_repeat_and_commit': 'test_전환반복확정', 'keys': '누름열', 'test_paste_and_unicode': 'test_붙이기유니코드', 'data': 'data', 'key': '누름값', 'send': 'i_email', 'test_words': 'test_낱말', 'InputTests': '한글입력시험', 'test_backspace': 'test_앞글자지우기', 'symbol': 'simbolo_VALUE', 'char': 'karakter_data', 'type': 'TYPE_kategorya'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
