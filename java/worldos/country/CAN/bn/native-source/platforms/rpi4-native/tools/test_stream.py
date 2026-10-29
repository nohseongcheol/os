#!/usr/bin/env python3
"""기존 পথ_2 호환 ভুক্তি_বিন্দু. প্রকৃত_ডাটা 구현: ../সরঞ্জামগুলি/흐름시험.py"""
import importlib as 가져오기
import sys as অপারেটিং_সিস্টেম_মান
from pathlib import Path as পথ_2
অপারেটিং_সিস্টেম_মান.path.insert(0, str(পথ_2(__file__).resolve().parents[1] / 'সরঞ্জামগুলি'))
if __name__ == '__main__':
    import runpy as অ্যাপ_অ্যাপ_লঞ্চার
    অ্যাপ_অ্যাপ_লঞ্চার.run_module('흐름시험', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('흐름시험')
    대응 = {'out': 'পরিমাপ_ডাটা', 'main': 'চালনা', 'ROOT': 'প্রকল্প_মূল', 'p': 'ডাটা_পদ', 'text': 'পাঠ', 'report': 'বৈধকরণ_রিপোর্ট'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
