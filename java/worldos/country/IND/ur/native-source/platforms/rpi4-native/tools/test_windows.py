#!/usr/bin/env python3
"""기존 راستہ_2 호환 اندراج_نقطہ. اصل_کوائف 구현: ../ٹولز/창시험.py"""
import importlib as 가져오기
import sys as آپریٹنگ_سسٹم_قدر
from pathlib import Path as راستہ_2
آپریٹنگ_سسٹم_قدر.path.insert(0, str(راستہ_2(__file__).resolve().parents[1] / 'ٹولز'))
if __name__ == '__main__':
    import runpy as ایپ_ایپ_دراز
    ایپ_ایپ_دراز.run_module('창시험', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('창시험')
    대응 = {'wait': '기다리기', 'x': 'ایکس_مربوط', 's': 'سلک_کوائف', 'xy': 'معدد_جوڑا', 'sel': 'منتخب_کنندہ_a916db4e', 'seconds': '초단위', 'log': 'لاگ_صف', 'at': '현재위치', 'send': 'بھیجیں', 'main': 'چلائیں', 'req': '요청값', 'hot': 'تیز_راہ_قدر', 'pump': 'ہینڈل_ایونٹ', 'ROOT': 'عکس_ڈالنا_روٹ', 'marker': '확인표시', 'b': '둘째값', 'command': 'حکم', 'shell': 'شیل', 'f': 'فائل_اندراج', 'color': '색상', 'click': 'کلک_بٹن', 'k': '셋째순번', 'c': 'کریکٹر_ضابطہ', 'r': '반환값', 'p': 'کوائف_پوزیشن_ٹھیک_کریں', 'done': '완료량', 'end': 'اختتام_آفسٹ', 'command_mode': 'حکم_موڈ', 'key': '누름값', 'y': '세로좌표', 'pixels': '화소들', 'result': 'پیمائش', 'report': 'توثیق_رپورٹ', 'dest': 'منزل_مقصود_قدر_پوزیشن_ٹھیک_کریں', 'work': '작업경로', 'qmp': '모의제어접속'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
