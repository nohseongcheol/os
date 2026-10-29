#!/usr/bin/env python3
"""기존 يول 호환 كىرگۈزۈش_نوقتا. ھەقىقىي_مەلۇمات 구현: ../قوراللار/يۈكلىمەك_ھۆججەت.py"""
import importlib as 가져오기
import sys as مەشغۇلات_سىستېمىسى_قىممىتى
from pathlib import Path as يول
مەشغۇلات_سىستېمىسى_قىممىتى.path.insert(0, str(يول(__file__).resolve().parents[1] / 'قوراللار'))
if __name__ == '__main__':
    import runpy as ئەپ_خادىم
    ئەپ_خادىم.run_module('يۈكلىمەك_ھۆججەت', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('يۈكلىمەك_ھۆججەت')
    대응 = {'data': 'مەلۇمات', 'i': '순번', 'name': 'ئاتى', 'c': 'ھەرپ_كودى', 'p': 'مەلۇمات_ئورۇنلاشتۇرۇش', 'args': 'دەلىل_رەت'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
