#!/usr/bin/env python3
"""기존 পথ_2 호환 ভুক্তি_বিন্দু. প্রকৃত_ডাটা 구현: ../সরঞ্জামগুলি/গঠন_নেটওয়ার্ক.py"""
import importlib as 가져오기
import sys as অপারেটিং_সিস্টেম_মান
from pathlib import Path as পথ_2
অপারেটিং_সিস্টেম_মান.path.insert(0, str(পথ_2(__file__).resolve().parents[1] / 'সরঞ্জামগুলি'))
if __name__ == '__main__':
    import runpy as অ্যাপ_অ্যাপ_লঞ্চার
    অ্যাপ_অ্যাপ_লঞ্চার.run_module('গঠন_নেটওয়ার্ক', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('গঠন_নেটওয়ার্ক')
    대응 = {'obj': 'গন্তব্য_ফাইল', 'objects': 'গন্তব্য_ফাইলগুলি', 'library': 'লাইব্রেরি', 'output': '출력결과', 'port': 'পোর্ট_নম্বর', 'root': 'মূল_ইমেইল', 'files': 'ফাইল_তালিকা', 'source': '원본자료', 'run': 'কার্যকর_করুন_আদেশ', 'flags': 'বিন্যাসন_ব্যাকগ্রাউন্ড_ইনটেলিজেন্ট_ট্র্যান্সফার_সার্ভিস', 'path': 'পথ_2', 'build_network': 'ক্রিয়েট_নেটওয়ার্ক', 'cc': '시언어번역기', 'ar': 'সংগ্রহ_করা_টুল'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
