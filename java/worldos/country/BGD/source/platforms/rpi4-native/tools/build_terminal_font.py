#!/usr/bin/env python3
"""기존 পথ_2 호환 ভুক্তি_বিন্দু. প্রকৃত_ডাটা 구현: ../সরঞ্জামগুলি/গঠন_টার্মিনাল_হরফ.py"""
import importlib as 가져오기
import sys as অপারেটিং_সিস্টেম_মান
from pathlib import Path as পথ_2
অপারেটিং_সিস্টেম_মান.path.insert(0, str(পথ_2(__file__).resolve().parents[1] / 'সরঞ্জামগুলি'))
if __name__ == '__main__':
    import runpy as অ্যাপ_অ্যাপ_লঞ্চার
    অ্যাপ_অ্যাপ_লঞ্চার.run_module('গঠন_টার্মিনাল_হরফ', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('গঠন_টার্মিনাল_হরফ')
    대응 = {'data': 'ডাটা', 'img': 'অঙ্কন_মান', 'bits': 'ব্যাকগ্রাউন্ড_ইনটেলিজেন্ট_ট্র্যান্সফার_সার্ভিস_তালিকা', 'x': 'X_বোতাম_অক্ষবিন্দু', 'draw': '화면그리기', 'licences': '이용허락목록', 'paths': 'পথ_তালিকা', 'y': 'Y_বোতাম_অক্ষবিন্দু', 'main': 'চালনা', 'src': '원본주소', 'fonts': 'হরফ_তালিকা', 'ROOT': 'প্রকল্প_মূল', 'p': 'ডাটা_পদ', 'cp': 'অক্ষর_এনকোড_করা', 'target': 'লক্ষ্য'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
