#!/usr/bin/env python3
"""기존 পথ_2 호환 ভুক্তি_বিন্দু. প্রকৃত_ডাটা 구현: ../সরঞ্জামগুলি/কার্যকর_করুন_আদেশ.py"""
import importlib as 가져오기
import sys as অপারেটিং_সিস্টেম_মান
from pathlib import Path as পথ_2
অপারেটিং_সিস্টেম_মান.path.insert(0, str(পথ_2(__file__).resolve().parents[1] / 'সরঞ্জামগুলি'))
if __name__ == '__main__':
    import runpy as অ্যাপ_অ্যাপ_লঞ্চার
    অ্যাপ_অ্যাপ_লঞ্চার.run_module('কার্যকর_করুন_আদেশ', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('কার্যকর_করুন_আদেশ')
    대응 = {'supported': '지원목록', 'parser': 'পার্সার', 'qemu': '모의기계', 'run_desktop': 'রান_ডেস্কটপ', 'main': 'চালনা', 'host': 'হোস্ট', 'status': 'অবস্হা_মান', 'NetworkBridge': 'নেটওয়ার্ক_ব্রিজ', 'ROOT': 'প্রকল্প_মূল', 'bridge': 'ব্রিজ', 'loader': '적재기', 'base': 'পটভূমি_মান', 'options': 'পছন্দ', 'binary': 'বাইনারি', 'args': 'যুক্তি_অ্যারে', 'command': 'আদেশ'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
