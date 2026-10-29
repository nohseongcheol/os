#!/usr/bin/env python3
"""기존 পথ_2 호환 ভুক্তি_বিন্দু. প্রকৃত_ডাটা 구현: ../সরঞ্জামগুলি/গঠন_সিস্টেম.py"""
import importlib as 가져오기
import sys as অপারেটিং_সিস্টেম_মান
from pathlib import Path as পথ_2
অপারেটিং_সিস্টেম_মান.path.insert(0, str(পথ_2(__file__).resolve().parents[1] / 'সরঞ্জামগুলি'))
if __name__ == '__main__':
    import runpy as অ্যাপ_অ্যাপ_লঞ্চার
    অ্যাপ_অ্যাপ_লঞ্চার.run_module('গঠন_সিস্টেম', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('গঠন_সিস্টেম')
    대응 = {'network': 'নেটওয়ার্ক_9b2e3222', 'BUILD': 'গঠন_পথ', 'ar': 'সংগ্রহ_করা_টুল', 'build_examples': '예제만들기', 'posix': '포직스경로', 'font_data': 'হরফ_ডাটা', 'flags': 'বিন্যাসন_ব্যাকগ্রাউন্ড_ইনটেলিজেন্ট_ট্র্যান্সফার_সার্ভিস', 'a': '첫째값', 'cc': '시언어번역기', 'args': 'যুক্তি_অ্যারে', 'source_flags': '원본설정', 'ld': '연결편집기', 'method': 'পদ্ধতি_ভুক্তি', 'main': 'চালনা', 'objcopy': 'বস্তু_ফাইল_পরিবর্তক', 'ROOT': 'প্রকল্প_মূল', 'cxx': '시플플번역기', 'includes': '포함인수', 'compiler': '번역기', 'build_users': 'ক্রিয়েট_ব্যবহারকারী_স্পেস', 'f': 'ফাইল_ভুক্তি', 'extra': '추가영역', 'exports': 'রপ্তানি_সারণি', 'jobs': '빌드작업', 'run': 'কার্যকর_করুন_আদেশ', 'path': 'পথ_2', 'REPO': 'সংগ্রহস্থলের_মূল', 'tool': 'সরঞ্জামগুলি', 'classes': 'শ্রেণী_পথ', 'output': '출력결과', 'samples': '예제들', 'symbol': 'প্রতীক_মান', 'source': '원본자료', 'name': 'নাম', 'build_network': 'ক্রিয়েট_নেটওয়ার্ক', 'font_info': 'হরফ_তথ্য', 'manifest': '꾸러미명세', 'work': '작업경로'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
