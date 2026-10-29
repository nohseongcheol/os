#!/usr/bin/env python3
"""기존 পথ_2 호환 ভুক্তি_বিন্দু. প্রকৃত_ডাটা 구현: ../সরঞ্জামগুলি/গঠন_ব্যবহারকারী_স্পেস.py"""
import importlib as 가져오기
import sys as অপারেটিং_সিস্টেম_মান
from pathlib import Path as পথ_2
অপারেটিং_সিস্টেম_মান.path.insert(0, str(পথ_2(__file__).resolve().parents[1] / 'সরঞ্জামগুলি'))
if __name__ == '__main__':
    import runpy as অ্যাপ_অ্যাপ_লঞ্চার
    অ্যাপ_অ্যাপ_লঞ্চার.run_module('গঠন_ব্যবহারকারী_স্পেস', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('গঠন_ব্যবহারকারী_স্পেস')
    대응 = {'mode': 'পদ্ধতি_মোড', 'header': 'হেডার_মান', 'i': '순번', 'build_ccompiler': '시언어번역기만들기', 'ar': 'সংগ্রহ_করা_টুল', 'posix': '포직스경로', 'payload': 'পেলোড_ডাটা', 'flags': 'বিন্যাসন_ব্যাকগ্রাউন্ড_ইনটেলিজেন্ট_ট্র্যান্সফার_সার্ভিস', 'cases': '시험사례', 'cc': '시언어번역기', 'data': 'ডাটা', 'build_java_library': '자바라이브러리만들기', 'ld': '연결편집기', 'repo': 'সংগ্রহস্থলের_পথ', 'build_python': '파이썬만들기', 'inc': '포함경로', 'argument': '전달값', 'text': 'পাঠ', 'headers': 'হেডার_তালিকা', 'cxx': '시플플번역기', 'valid': '유효함', 'build': 'গঠন', 'build_users': 'ক্রিয়েট_ব্যবহারকারী_স্পেস', 'compiler': '번역기', 'uzlib': '압축해제경로', 'extra': '추가영역', 'phoff': 'অ্যাপ_হেডার_অফসেট', 'offset': 'অফসেট_মান', 'text_address': 'আদেশ_ইমেইল', 'abi': '호출규약', 'assembly': '어셈블리자료', 'run': 'কার্যকর_করুন_আদেশ', 'path': 'পথ_2', 'p': 'ডাটা_পদ', 'changed': '바뀐자료', 'n': '개수', 'flag': 'সেটিংস_মান', 'index': 'লুকআপ_সূচি', 'classes': 'শ্রেণী_পথ', 'output': '출력결과', 'loads': '적재구획', 'data_address': 'ডাটা_ইমেইল', 'symbol': 'প্রতীক_মান', 'root': 'মূল_ইমেইল', 'patches': '수정사항', 'source': '원본자료', 'sizes': '크기목록', 'blobs': '탑재덩이들', 'name': 'নাম', 'value': 'মান', 'fmt': 'বিন্যাস_932e03c8', 'work': '작업경로'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
