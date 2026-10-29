#!/usr/bin/env python3
"""기존 পথ 호환 প্রবিষ্ট_পইণ্ট. প্ৰকৃত_ডাটা 구현: ../সঁজুলিসমূহ/되돌림시험서버.py"""
import importlib as 가져오기
import sys as অপাৰেটিং_ছিষ্টেম_মান
from pathlib import Path as পথ
অপাৰেটিং_ছিষ্টেম_মান.path.insert(0, str(পথ(__file__).resolve().parents[1] / 'সঁজুলিসমূহ'))
if __name__ == '__main__':
    import runpy as এপ্প্_এপ্প্_ড্ৰৱাৰ
    এপ্প্_এপ্প্_ড্ৰৱাৰ.run_module('되돌림시험서버', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('되돌림시험서버')
    대응 = {'data': 'ডাটা', 'e': '보조항목', 'connection': 'সংযোগ_e05f319b', 'f': 'ফাইল_প্রবিষ্ট', 'peer': 'পীয়েৰ_মান', 'self': '자신', 'udp': '전문제어', 't': 'টাৰ্মিনেল_প্রবিষ্ট', 'tcp': 'সংযোগ_নিয়ন্ত্রণ', 'EchoFixture': '되돌림시험서버', 'args': 'যুক্তি_শৃঙ্খলা', 'chunk': '조각'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
