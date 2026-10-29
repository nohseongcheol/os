#!/usr/bin/env python3
"""기존 راههه 호환 داخلا_هنڌ. اصلي_ڪوائف 구현: ../اوزار/تعميل_ڪرڻ_حڪم.py"""
import importlib as 가져오기
import sys as آپريٽنگ_سسٽم_قدر
from pathlib import Path as راههه
آپريٽنگ_سسٽم_قدر.path.insert(0, str(راههه(__file__).resolve().parents[1] / 'اوزار'))
if __name__ == '__main__':
    import runpy as ائپ_ائپ_ڊرائر
    ائپ_ائپ_ڊرائر.run_module('تعميل_ڪرڻ_حڪم', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('تعميل_ڪرڻ_حڪم')
    대응 = {'supported': '지원목록', 'parser': '인수해석기', 'qemu': '모의기계', 'run_desktop': 'هلائڻ_ڊيسڪٽاپ', 'main': 'هلائڻ', 'host': 'مهمان', 'status': 'حالت_قدر', 'NetworkBridge': '통신다리', 'ROOT': '기준', 'bridge': '연결다리', 'loader': '적재기', 'base': 'پس_منظر_قدر', 'options': 'اختيار', 'binary': 'ٻٽو', 'args': 'دليل_ترتيب', 'command': 'حڪم'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
