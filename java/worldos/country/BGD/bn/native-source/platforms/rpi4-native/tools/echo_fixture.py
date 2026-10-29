#!/usr/bin/env python3
"""기존 পথ_2 호환 ভুক্তি_বিন্দু. প্রকৃত_ডাটা 구현: ../সরঞ্জামগুলি/되돌림시험서버.py"""
import importlib as 가져오기
import sys as অপারেটিং_সিস্টেম_মান
from pathlib import Path as পথ_2
অপারেটিং_সিস্টেম_মান.path.insert(0, str(পথ_2(__file__).resolve().parents[1] / 'সরঞ্জামগুলি'))
if __name__ == '__main__':
    import runpy as অ্যাপ_অ্যাপ_লঞ্চার
    অ্যাপ_অ্যাপ_লঞ্চার.run_module('되돌림시험서버', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('되돌림시험서버')
    대응 = {'data': 'ডাটা', 'e': '보조항목', 'connection': 'সংযোগ_e05f319b', 'f': 'ফাইল_ভুক্তি', 'peer': 'পিয়ার_মান', 'self': '자신', 'udp': '전문제어', 't': 'টার্মিনাল_ভুক্তি', 'tcp': 'সংযোগ_নিয়ন্ত্রণ', 'EchoFixture': '되돌림시험서버', 'args': 'যুক্তি_অ্যারে', 'chunk': '조각'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
