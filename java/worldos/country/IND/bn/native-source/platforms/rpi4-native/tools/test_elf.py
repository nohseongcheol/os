#!/usr/bin/env python3
"""기존 পথ_2 호환 ভুক্তি_বিন্দু. প্রকৃত_ডাটা 구현: ../সরঞ্জামগুলি/실행파일시험.py"""
import importlib as 가져오기
import sys as অপারেটিং_সিস্টেম_মান
from pathlib import Path as পথ_2
অপারেটিং_সিস্টেম_মান.path.insert(0, str(পথ_2(__file__).resolve().parents[1] / 'সরঞ্জামগুলি'))
if __name__ == '__main__':
    import runpy as অ্যাপ_অ্যাপ_লঞ্চার
    অ্যাপ_অ্যাপ_লঞ্চার.run_module('실행파일시험', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('실행파일시험')
    대응 = {'out': 'পরিমাপ_ডাটা', 'expected': '예상결과', 'phoff': 'অ্যাপ_হেডার_অফসেট', 'offset': 'অফসেট_মান', 'invalid': 'অবৈধ_ডাটা', 'path': 'পথ_2', 'executable': '실행가능파일', 'rejected': '거부결과', 'linux_example': '리눅스예제', 'original': '원본', 'result': 'পরিমাপ', 'format_': 'বিন্যাস_b87fd068', 'main': 'চালনা', 'content': 'সামগ্রি_মান', 'source': '원본자료', 'name': 'নাম', 'reference': 'তুলনা_বেসলাইন', 'ROOT': 'প্রকল্প_মূল', 'value': 'মান', 'report': 'বৈধকরণ_রিপোর্ট'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
