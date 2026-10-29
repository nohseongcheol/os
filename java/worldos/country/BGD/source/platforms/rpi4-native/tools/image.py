#!/usr/bin/env python3
"""기존 পথ_2 호환 ভুক্তি_বিন্দু. প্রকৃত_ডাটা 구현: ../সরঞ্জামগুলি/ক্রিয়েট_ছবি.py"""
import importlib as 가져오기
import sys as অপারেটিং_সিস্টেম_মান
from pathlib import Path as পথ_2
অপারেটিং_সিস্টেম_মান.path.insert(0, str(পথ_2(__file__).resolve().parents[1] / 'সরঞ্জামগুলি'))
if __name__ == '__main__':
    import runpy as অ্যাপ_অ্যাপ_লঞ্চার
    অ্যাপ_অ্যাপ_লঞ্চার.run_module('ক্রিয়েট_ছবি', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('ক্রিয়েট_ছবি')
    대응 = {'total': '총량', 'start': 'চালনা', 'firmware': '기초제어프로그램', 'files': 'ফাইল_তালিকা', 'archive_base': '압축기준', 'partition': 'বিভাজন_ফাইল', 'archive': 'সংগ্রহ_করা', 'main': 'চালনা', 'block': 'ডাটা_আটক_করা', 'ROOT': 'প্রকল্প_মূল', 'boot': '부팅경로', 'stage': 'স্টেজ_মান', 'out': 'পরিমাপ_ডাটা', 'expected': '예상결과', 'f': 'ফাইল_ভুক্তি', 'src': '원본주소', 'path': 'পথ_2', 'p': 'ডাটা_পদ', 'extracted': '추출자료', 'member': 'সদস্য', 'mbr': '주부트기록', 'image': 'ছবি', 'sector_count': '섹터개수', 'dist': '배포경로', 'sha': '해시계산', 'license_': 'লাইসেন্স', 'source': '원본자료', 'name': 'নাম', 'value': 'মান', 'manifest': '꾸러미명세', 'dest': 'গন্তব্য_মান_পদ', 'work': '작업경로'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
