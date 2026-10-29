#!/usr/bin/env python3
"""기존 পথ_2 호환 ভুক্তি_বিন্দু. প্রকৃত_ডাটা 구현: ../সরঞ্জামগুলি/셸시험.py"""
import importlib as 가져오기
import sys as অপারেটিং_সিস্টেম_মান
from pathlib import Path as পথ_2
অপারেটিং_সিস্টেম_মান.path.insert(0, str(পথ_2(__file__).resolve().parents[1] / 'সরঞ্জামগুলি'))
if __name__ == '__main__':
    import runpy as অ্যাপ_অ্যাপ_লঞ্চার
    অ্যাপ_অ্যাপ_লঞ্চার.run_module('셸시험', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('셸시험')
    대응 = {'timeout': '시간제한', 'x': 'X_বোতাম_অক্ষবিন্দু', 'msg': 'নেটওয়ার্ক_ইমেইল', 'i': '순번', 'reply': 'উত্তর_দিন', 'call': '호출', 'args': 'যুক্তি_অ্যারে', 'chunk': '조각', 'data': 'ডাটা', 'proc': 'প্রসেস', 'long_text': '긴글', 'restored': '복원자료', 'send': 'পাঠান', 'file': 'নথির_নাম', 'main': 'চালনা', 'found': 'দেখুন_পরিমাপ', 'ROOT': 'প্রকল্প_মূল', 'text': 'পাঠ', 'marker': '확인표시', 'command': 'আদেশ', 'expected': '예상결과', 'pixel': 'পেল্', 'shell': 'শেল', 'poll': '준비살피미', 'transcript': '대화기록', 'end': 'শেষ_করা_অফসেট', 'image': 'ছবি', 'key': '누름값', 'y': 'Y_বোতাম_অক্ষবিন্দু', 'output': '출력결과', 'result': 'পরিমাপ', 'client': 'গ্রাহক', 'line': 'নিবেশের_পঙ্_ক্তি', 'stream': 'প্রবাহ_মান', 'name': 'নাম', 'value': 'মান', 'receive': '수신하기', 'report': 'বৈধকরণ_রিপোর্ট', 'work': '작업경로', 'qmp': '모의제어접속'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
