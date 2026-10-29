#!/usr/bin/env python3
"""기존 گوزەر 호환 تێنووسین_خاڵ. ڕاستەکی_دەیتا 구현: ../ئامرازەکان/جێبەجێکردن_فەرمان.py"""
import importlib as 가져오기
import sys as سیستەمی_کارپێکردن_نرخ
from pathlib import Path as گوزەر
سیستەمی_کارپێکردن_نرخ.path.insert(0, str(گوزەر(__file__).resolve().parents[1] / 'ئامرازەکان'))
if __name__ == '__main__':
    import runpy as بەرنامە_ئەندامی_ستاف
    بەرنامە_ئەندامی_ستاف.run_module('جێبەجێکردن_فەرمان', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('جێبەجێکردن_فەرمان')
    대응 = {'supported': '지원목록', 'parser': '인수해석기', 'qemu': '모의기계', 'run_desktop': 'ڕادان_دێسکتۆپ', 'main': 'ڕادان', 'host': 'جێدەر', 'status': 'دۆخ_نرخ', 'NetworkBridge': '통신다리', 'ROOT': '기준', 'bridge': '연결다리', 'loader': '적재기', 'base': 'بن_زمینه_نرخ', 'options': 'بەربژارەکان', 'binary': 'دوانەیی', 'args': 'ئارگیومێنت_ڕیزی_داتا', 'command': 'فەرمان'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
