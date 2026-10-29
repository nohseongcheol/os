#!/usr/bin/env python3
"""기존 راههه 호환 داخلا_هنڌ. اصلي_ڪوائف 구현: ../اوزار/تعميل_ڪرڻ_فائل.py"""
import importlib as 가져오기
import sys as آپريٽنگ_سسٽم_قدر
from pathlib import Path as راههه
آپريٽنگ_سسٽم_قدر.path.insert(0, str(راههه(__file__).resolve().parents[1] / 'اوزار'))
if __name__ == '__main__':
    import runpy as ائپ_ائپ_ڊرائر
    ائپ_ائپ_ڊرائر.run_module('تعميل_ڪرڻ_فائل', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('تعميل_ڪرڻ_فائل')
    대응 = {'timeout': '시간제한', 's': 'اسٽرنگ_ڪوائف', 'i': '순번', 'match': '일치', 'files': 'فائل_فهرست', 'program': 'ائپ', 'executable': '실행가능파일', 'args': 'دليل_ترتيب', 'chunk': '조각', 'data': 'ڪوائف', 'proc': 'عمل_a7054519', 'send': 'اي_ميل', 'main': 'هلائڻ', 'marker': '확인표시', 'command': 'حڪم', 'include': '포함항목', 'dumped': '갈무리자료', 'run': 'تعميل_ڪرڻ_حڪم', 'p': '자료위치', 'parser': '인수해석기', 'options': 'اختيار', 'kind': 'قسم_قدر_4b6d6445', 'selector': 'چونڊيندڙ', 'upload_data': 'اپ_لوڊ_ڪريو_ڪوائف', 'end': 'ختم_ڪريو_آف_سيٽ', 'n': '개수', 'd': 'منزل_مقصود_ڪوائف', 'key': '누름값', 'output': '출력결과', 'line': 'لڪير', 'name': 'نالو', 'upload_name': 'اپ_لوڊ_ڪريو_نالو', 'receive': '수신하기'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
