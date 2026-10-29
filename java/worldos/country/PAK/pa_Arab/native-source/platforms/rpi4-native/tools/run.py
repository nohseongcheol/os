#!/usr/bin/env python3
"""기존 راہ 호환 داخلہ_مقام. اصلی_کوائف 구현: ../اوزار/نفاذ_کرو_حکم.py"""
import importlib as 가져오기
import sys as آپریٹنگ_سسٹم_قدر
from pathlib import Path as راہ
آپریٹنگ_سسٹم_قدر.path.insert(0, str(راہ(__file__).resolve().parents[1] / 'اوزار'))
if __name__ == '__main__':
    import runpy as ایپ_عملے_دا_رکن
    ایپ_عملے_دا_رکن.run_module('نفاذ_کرو_حکم', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('نفاذ_کرو_حکم')
    대응 = {'supported': '지원목록', 'parser': '인수해석기', 'qemu': '모의기계', 'run_desktop': 'چلاؤ_ڈیسک_ٹاپ', 'main': 'چلاؤ', 'host': 'مہمان_b78e430d', 'status': 'حالت_قدر', 'NetworkBridge': 'نیٹ_ورک_برج', 'ROOT': '기준', 'bridge': 'برج', 'loader': '적재기', 'base': 'پس_منظر_قدر', 'options': 'اختیار', 'binary': 'مثنی', 'args': 'دلیل_ایرے', 'command': 'حکم'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
