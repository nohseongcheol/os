#!/usr/bin/env python3
"""기존 گوزەر 호환 تێنووسین_خاڵ. ڕاستەکی_دەیتا 구현: ../ئامرازەکان/창시험.py"""
import importlib as 가져오기
import sys as سیستەمی_کارپێکردن_نرخ
from pathlib import Path as گوزەر
سیستەمی_کارپێکردن_نرخ.path.insert(0, str(گوزەر(__file__).resolve().parents[1] / 'ئامرازەکان'))
if __name__ == '__main__':
    import runpy as بەرنامە_ئەندامی_ستاف
    بەرنامە_ئەندامی_ستاف.run_module('창시험', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('창시험')
    대응 = {'wait': '기다리기', 'x': 'پۆوتانی_x', 's': 'رست_دەیتا', 'xy': 'جووتی_ڕێکخستن', 'sel': 'هەڵبژێرەر_a916db4e', 'seconds': '초단위', 'log': 'تۆمار_ڕزن', 'at': '현재위치', 'send': 'ناردن', 'main': 'ڕادان', 'req': '요청값', 'hot': 'کورتەڕێ_نرخ', 'pump': 'دەسک_پێشهات', 'ROOT': '기준', 'marker': '확인표시', 'b': '둘째값', 'command': 'فەرمان', 'shell': 'توێکڵ', 'f': 'فایل_تێنووسین', 'color': '색상', 'click': 'کرته_کردن_دوگمه', 'k': '셋째순번', 'c': 'کۆدی_نووسە', 'r': '반환값', 'p': '자료위치', 'done': '완료량', 'end': 'دوایی_کردن_ئۆفسێت', 'command_mode': 'فەرمان_دۆخ', 'key': '누름값', 'y': '세로좌표', 'pixels': '화소들', 'result': '결과', 'report': 'ڕەواکردن_ڕاپۆرت', 'dest': '목적위치', 'work': '작업경로', 'qmp': '모의제어접속'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
