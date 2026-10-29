#!/usr/bin/env python3
"""기존 يول 호환 كىرگۈزۈش_نوقتا. ھەقىقىي_مەلۇمات 구현: ../قوراللار/ئىجرا_قىلىش_بۇيرۇق.py"""
import importlib as 가져오기
import sys as مەشغۇلات_سىستېمىسى_قىممىتى
from pathlib import Path as يول
مەشغۇلات_سىستېمىسى_قىممىتى.path.insert(0, str(يول(__file__).resolve().parents[1] / 'قوراللار'))
if __name__ == '__main__':
    import runpy as ئەپ_خادىم
    ئەپ_خادىم.run_module('ئىجرا_قىلىش_بۇيرۇق', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('ئىجرا_قىلىش_بۇيرۇق')
    대응 = {'supported': '지원목록', 'parser': '인수해석기', 'qemu': '모의기계', 'run_desktop': 'قوزغىتىش_ئۈستەليۈزى', 'main': 'ئىجرا_قىل_2', 'host': 'باقار', 'status': 'ھالەت_قىممىتى', 'NetworkBridge': 'تور_كۆۋرۈك', 'ROOT': 'كۆرسىتىش_يىلتىز', 'bridge': 'كۆۋرۈك', 'loader': '적재기', 'base': 'تەگلىك_قىممىتى', 'options': 'تاللانمىلار', 'binary': 'ئىككىلىك', 'args': 'دەلىل_رەت', 'command': 'بۇيرۇق'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
