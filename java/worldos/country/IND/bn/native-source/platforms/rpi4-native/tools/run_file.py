#!/usr/bin/env python3
"""기존 পথ_2 호환 ভুক্তি_বিন্দু. প্রকৃত_ডাটা 구현: ../সরঞ্জামগুলি/কার্যকর_করুন_ফাইল.py"""
import importlib as 가져오기
import sys as অপারেটিং_সিস্টেম_মান
from pathlib import Path as পথ_2
অপারেটিং_সিস্টেম_মান.path.insert(0, str(পথ_2(__file__).resolve().parents[1] / 'সরঞ্জামগুলি'))
if __name__ == '__main__':
    import runpy as অ্যাপ_অ্যাপ_লঞ্চার
    অ্যাপ_অ্যাপ_লঞ্চার.run_module('কার্যকর_করুন_ফাইল', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('কার্যকর_করুন_ফাইল')
    대응 = {'timeout': '시간제한', 's': 'স্ট্রিং_ডাটা', 'i': '순번', 'match': '일치', 'files': 'ফাইল_তালিকা', 'program': 'অ্যাপ', 'executable': '실행가능파일', 'args': 'যুক্তি_অ্যারে', 'chunk': '조각', 'data': 'ডাটা', 'proc': 'প্রসেস', 'send': 'পাঠান', 'main': 'চালনা', 'marker': '확인표시', 'command': 'আদেশ', 'include': '포함항목', 'dumped': '갈무리자료', 'run': 'কার্যকর_করুন_আদেশ', 'p': 'ডাটা_পদ', 'parser': 'পার্সার', 'options': 'পছন্দ', 'kind': 'বিভাগ_মান', 'selector': 'নির্বাচক', 'upload_data': 'আপলোড_ডাটা', 'end': 'শেষ_করা_অফসেট', 'n': '개수', 'd': 'গন্তব্য_ডাটা', 'key': '누름값', 'output': '출력결과', 'line': 'নিবেশের_পঙ্_ক্তি', 'name': 'নাম', 'upload_name': 'আপলোড_নাম', 'receive': '수신하기'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
