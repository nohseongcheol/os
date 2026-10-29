#!/usr/bin/env python3
"""기존 راستہ_2 호환 اندراج_نقطہ. اصل_کوائف 구현: ../ٹولز/نفاذ_کریں_حکم.py"""
import importlib as 가져오기
import sys as آپریٹنگ_سسٹم_قدر
from pathlib import Path as راستہ_2
آپریٹنگ_سسٹم_قدر.path.insert(0, str(راستہ_2(__file__).resolve().parents[1] / 'ٹولز'))
if __name__ == '__main__':
    import runpy as ایپ_ایپ_دراز
    ایپ_ایپ_دراز.run_module('نفاذ_کریں_حکم', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('نفاذ_کریں_حکم')
    대응 = {'supported': '지원목록', 'parser': '인수해석기', 'qemu': '모의기계', 'run_desktop': 'چلائیں_ڈیسک_ٹاپ', 'main': 'چلائیں', 'host': 'میزبان', 'status': 'حالت_قدر', 'NetworkBridge': 'نیٹ_ورک_برج', 'ROOT': 'عکس_ڈالنا_روٹ', 'bridge': 'برج', 'loader': '적재기', 'base': 'پس_منظر_قدر', 'options': 'اختیارات', 'binary': 'ثنائی', 'args': 'دلائل_لڑی', 'command': 'حکم'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
