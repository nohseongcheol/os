#!/usr/bin/env python3
"""기존 পথ_2 호환 ভুক্তি_বিন্দু. প্রকৃত_ডাটা 구현: ../সরঞ্জামগুলি/예제빌드.py"""
import importlib as 가져오기
import sys as অপারেটিং_সিস্টেম_মান
from pathlib import Path as পথ_2
অপারেটিং_সিস্টেম_মান.path.insert(0, str(পথ_2(__file__).resolve().parents[1] / 'সরঞ্জামগুলি'))
if __name__ == '__main__':
    import runpy as অ্যাপ_অ্যাপ_লঞ্চার
    অ্যাপ_অ্যাপ_লঞ্চার.run_module('예제빌드', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('예제빌드')
    대응 = {'out': 'পরিমাপ_ডাটা', 'build_examples': '예제만들기', 'files': 'ফাইল_তালিকা', 'java': '자바실행', 'run': 'কার্যকর_করুন_আদেশ', 'path': 'পথ_2', 'p': 'ডাটা_পদ', 'readme': 'স্বনিবন্ধ', 'build_java_library': '자바라이브러리만들기', 'code': '명령열', 'index': 'লুকআপ_সূচি', 'classes': 'শ্রেণী_পথ', 'repo': 'সংগ্রহস্থলের_পথ', 'root': 'মূল_ইমেইল', 'content': 'সামগ্রি_মান', 'source': '원본자료', 'name': 'নাম', 'target': 'লক্ষ্য', 'manifest': '꾸러미명세', 'language': 'ভাষা'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
