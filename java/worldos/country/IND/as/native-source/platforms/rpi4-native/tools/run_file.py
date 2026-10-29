#!/usr/bin/env python3
"""기존 পথ 호환 প্রবিষ্ট_পইণ্ট. প্ৰকৃত_ডাটা 구현: ../সঁজুলিসমূহ/নিষ্পাদন_ফাইল.py"""
import importlib as 가져오기
import sys as অপাৰেটিং_ছিষ্টেম_মান
from pathlib import Path as পথ
অপাৰেটিং_ছিষ্টেম_মান.path.insert(0, str(পথ(__file__).resolve().parents[1] / 'সঁজুলিসমূহ'))
if __name__ == '__main__':
    import runpy as এপ্প্_এপ্প্_ড্ৰৱাৰ
    এপ্প্_এপ্প্_ড্ৰৱাৰ.run_module('নিষ্পাদন_ফাইল', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('নিষ্পাদন_ফাইল')
    대응 = {'timeout': '시간제한', 's': 'ষ্ট্ৰিং_ডাটা', 'i': '순번', 'match': '일치', 'files': 'ফাইল_সূচী', 'program': 'এপ্প্', 'executable': '실행가능파일', 'args': 'যুক্তি_শৃঙ্খলা', 'chunk': '조각', 'data': 'ডাটা', 'proc': 'প্ৰসেস', 'send': 'ই_মেইল_কৰক', 'main': 'সঞ্চালন', 'marker': '확인표시', 'command': 'কমান্ড', 'include': '포함항목', 'dumped': '갈무리자료', 'run': 'নিষ্পাদন_আদেশ', 'p': 'ডাটা_স্থান_সলনি_কৰক', 'parser': '인수해석기', 'options': 'বিকল্প', 'kind': 'বর্গ_মান', 'selector': 'চয়নকাৰী', 'upload_data': 'আপল_ড_কৰক_ডাটা', 'end': 'অন্ত_কৰক_অফছেট', 'n': '개수', 'd': 'গন্তব্য_স্থান_ডাটা', 'key': '누름값', 'output': '출력결과', 'line': 'লাইন', 'name': 'নাম', 'upload_name': 'আপল_ড_কৰক_নাম', 'receive': '수신하기'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
