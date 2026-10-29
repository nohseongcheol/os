#!/usr/bin/env python3
"""기존 راہ 호환 داخلہ_مقام. اصلی_کوائف 구현: ../اوزار/화면요소시험.py"""
import importlib as 가져오기
import sys as آپریٹنگ_سسٹم_قدر
from pathlib import Path as راہ
آپریٹنگ_سسٹم_قدر.path.insert(0, str(راہ(__file__).resolve().parents[1] / 'اوزار'))
if __name__ == '__main__':
    import runpy as ایپ_عملے_دا_رکن
    ایپ_عملے_دا_رکن.run_module('화면요소시험', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('화면요소시험')
    대응 = {'wait': '기다리기', 'x': 'x_محدد', 's': 'سٹرنگ_کوائف', 'i': '순번', 'sel': 'منتخب_کرنڑ_آلا_a916db4e', 'seconds': '초단위', 'log': 'لاگ_صف', 'data': 'کوائف', 'at': '현재위치', 'send': 'بھیجو', 'main': 'چلاؤ', 'req': '요청값', 'hot': 'تیز_راہ_قدر', 'pump': 'نبٹنا_واقعہ', 'ROOT': '기준', 'marker': '확인표시', 'b': '둘째값', 'command': 'حکم', 'shell': 'شیل', 'f': 'فائل_داخلہ', 'click': 'کلک_کرو_بٹن', 'k': '셋째순번', 'c': 'کیریکٹر_کوڈ', 'r': '반환값', 'p': '자료위치', 'command_mode': 'حکم_موڈ', 'end': 'ختم_کرو_آف_سیٹ', 'classes': 'درجہ_راہ', 'key': '누름값', 'y': '세로좌표', 'result': '결과', 'report': 'جواز_دہی_رپورٹ', 'dest': '목적위치', 'work': '작업경로', 'qmp': '모의제어접속'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
