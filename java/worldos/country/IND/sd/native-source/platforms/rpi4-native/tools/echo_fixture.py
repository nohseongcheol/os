#!/usr/bin/env python3
"""기존 راههه 호환 داخلا_هنڌ. اصلي_ڪوائف 구현: ../اوزار/되돌림시험서버.py"""
import importlib as 가져오기
import sys as آپريٽنگ_سسٽم_قدر
from pathlib import Path as راههه
آپريٽنگ_سسٽم_قدر.path.insert(0, str(راههه(__file__).resolve().parents[1] / 'اوزار'))
if __name__ == '__main__':
    import runpy as ائپ_ائپ_ڊرائر
    ائپ_ائپ_ڊرائر.run_module('되돌림시험서버', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('되돌림시험서버')
    대응 = {'data': 'ڪوائف', 'e': '보조항목', 'connection': 'ڪنيڪشن_e05f319b', 'f': 'فائل_داخلا', 'peer': 'همعصر_قدر', 'self': '자신', 'udp': '전문제어', 't': '터미널항목', 'tcp': 'ڪنيڪشن_ڪنٽرول', 'EchoFixture': '되돌림시험서버', 'args': 'دليل_ترتيب', 'chunk': '조각'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
