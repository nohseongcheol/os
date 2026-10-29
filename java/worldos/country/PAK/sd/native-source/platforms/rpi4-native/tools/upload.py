#!/usr/bin/env python3
"""기존 راههه 호환 داخلا_هنڌ. اصلي_ڪوائف 구현: ../اوزار/اپ_لوڊ_ڪريو_فائلون.py"""
import importlib as 가져오기
import sys as آپريٽنگ_سسٽم_قدر
from pathlib import Path as راههه
آپريٽنگ_سسٽم_قدر.path.insert(0, str(راههه(__file__).resolve().parents[1] / 'اوزار'))
if __name__ == '__main__':
    import runpy as ائپ_ائپ_ڊرائر
    ائپ_ائپ_ڊرائر.run_module('اپ_لوڊ_ڪريو_فائلون', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('اپ_لوڊ_ڪريو_فائلون')
    대응 = {'data': 'ڪوائف', 'i': '순번', 'name': 'نالو', 'c': 'ڪئريڪٽر_ڪوڊ', 'p': '자료위치', 'args': 'دليل_ترتيب'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
