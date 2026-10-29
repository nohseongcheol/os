#!/usr/bin/env python3
"""기존 পথ_2 호환 ভুক্তি_বিন্দু. প্রকৃত_ডাটা 구현: ../সরঞ্জামগুলি/시언어번역기빌드.py"""
import importlib as 가져오기
import sys as অপারেটিং_সিস্টেম_মান
from pathlib import Path as পথ_2
অপারেটিং_সিস্টেম_মান.path.insert(0, str(পথ_2(__file__).resolve().parents[1] / 'সরঞ্জামগুলি'))
if __name__ == '__main__':
    import runpy as অ্যাপ_অ্যাপ_লঞ্চার
    অ্যাপ_অ্যাপ_লঞ্চার.run_module('시언어번역기빌드', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('시언어번역기빌드')
    대응 = {'out': 'পরিমাপ_ডাটা', 'builtins': '내장연산', 'header': 'হেডার_মান', 'sdk': '개발꾸러미', 'build_ccompiler': '시언어번역기만들기', 'i': '순번', 'elf': '실행파일', 'run': 'কার্যকর_করুন_আদেশ', 'flags': 'বিন্যাসন_ব্যাকগ্রাউন্ড_ইনটেলিজেন্ট_ট্র্যান্সফার_সার্ভিস', 'path': 'পথ_2', 'p': 'ডাটা_পদ', 'cc': '시언어번역기', 'obj': 'গন্তব্য_ফাইল', 'flag': 'সেটিংস_মান', 'ld': '연결편집기', 'objects': 'গন্তব্য_ফাইলগুলি', 'repo': 'সংগ্রহস্থলের_পথ', 'v': '임시값', 'upstream': 'আপস্ট্রীম', 'root': 'মূল_ইমেইল', 'assets': '탑재자료', 'source': '원본자료', 'name': 'নাম', 'includes': '포함인수'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
