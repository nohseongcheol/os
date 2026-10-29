#!/usr/bin/env python3
"""기존 পথ_2 호환 ভুক্তি_বিন্দু. প্রকৃত_ডাটা 구현: ../সরঞ্জামগুলি/자바가상기계시험.py"""
import importlib as 가져오기
import sys as অপারেটিং_সিস্টেম_মান
from pathlib import Path as পথ_2
অপারেটিং_সিস্টেম_মান.path.insert(0, str(পথ_2(__file__).resolve().parents[1] / 'সরঞ্জামগুলি'))
if __name__ == '__main__':
    import runpy as অ্যাপ_অ্যাপ_লঞ্চার
    অ্যাপ_অ্যাপ_লঞ্চার.run_module('자바가상기계시험', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('자바가상기계시험')
    대응 = {'message': '알림문', 's': 'স্ট্রিং_ডাটা', 'actual': 'প্রকৃত_পরিমাপ', 'match': '일치', 'payload': 'পেলোড_ডাটা', 'cases': '시험사례', 'fixture': '시험자료', 'main': 'চালনা', 'ROOT': 'প্রকল্প_মূল', 'text': 'পাঠ', 'valid': '유효함', 'includes': '포함인수', 'include': '포함항목', 'expected': '예상결과', 'sources': '원문목록', 'tmp': '임시경로', 'done': '완료량', 'classes': 'শ্রেণী_পথ', 'output': '출력결과', 'result': 'পরিমাপ', 'cmd': '명령인수', 'name': 'নাম', 'jar': '자바꾸러미', 'report': 'বৈধকরণ_রিপোর্ট', 'tests': '시험목록'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
