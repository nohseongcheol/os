#!/usr/bin/env python3
"""기존 পথ_2 호환 ভুক্তি_বিন্দু. প্রকৃত_ডাটা 구현: ../সরঞ্জামগুলি/자바라이브러리빌드.py"""
import importlib as 가져오기
import sys as অপারেটিং_সিস্টেম_মান
from pathlib import Path as পথ_2
অপারেটিং_সিস্টেম_মান.path.insert(0, str(পথ_2(__file__).resolve().parents[1] / 'সরঞ্জামগুলি'))
if __name__ == '__main__':
    import runpy as অ্যাপ_অ্যাপ_লঞ্চার
    অ্যাপ_অ্যাপ_লঞ্চার.run_module('자바라이브러리빌드', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('자바라이브러리빌드')
    대응 = {'header': 'হেডার_মান', 'sources': '원문목록', 'i': '순번', 'info': 'সিসটেম_তথ্য', 'payload': 'পেলোড_ডাটা', 'src': '원본주소', 'run': 'কার্যকর_করুন_আদেশ', 'build_java_library': '자바라이브러리만들기', 'relative': '상대경로', 'classes': 'শ্রেণী_পথ', 'dist': '배포경로', 'archive': 'সংগ্রহ_করা', 'output': '출력결과', 'root': 'মূল_ইমেইল', 'name': 'নাম', 'jar': '자바꾸러미', 'b': '둘째값', 'entries': '항목들'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
