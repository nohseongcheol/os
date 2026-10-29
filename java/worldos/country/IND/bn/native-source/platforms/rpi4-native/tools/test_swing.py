#!/usr/bin/env python3
"""기존 পথ_2 호환 ভুক্তি_বিন্দু. প্রকৃত_ডাটা 구현: ../সরঞ্জামগুলি/화면요소시험.py"""
import importlib as 가져오기
import sys as অপারেটিং_সিস্টেম_মান
from pathlib import Path as পথ_2
অপারেটিং_সিস্টেম_মান.path.insert(0, str(পথ_2(__file__).resolve().parents[1] / 'সরঞ্জামগুলি'))
if __name__ == '__main__':
    import runpy as অ্যাপ_অ্যাপ_লঞ্চার
    অ্যাপ_অ্যাপ_লঞ্চার.run_module('화면요소시험', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('화면요소시험')
    대응 = {'wait': '기다리기', 'x': 'X_বোতাম_অক্ষবিন্দু', 's': 'স্ট্রিং_ডাটা', 'i': '순번', 'sel': 'নির্বাচক_a916db4e', 'seconds': '초단위', 'log': 'লগ_সারি', 'data': 'ডাটা', 'at': '현재위치', 'send': 'পাঠান', 'main': 'চালনা', 'req': '요청값', 'hot': 'শর্টকাট_মান', 'pump': 'হাতল_ঘটনা', 'ROOT': 'প্রকল্প_মূল', 'marker': '확인표시', 'b': '둘째값', 'command': 'আদেশ', 'shell': 'শেল', 'f': 'ফাইল_ভুক্তি', 'click': 'ক্লিক_করা_বোতাম', 'k': '셋째순번', 'c': 'অক্ষর_কোড', 'r': '반환값', 'p': 'ডাটা_পদ', 'command_mode': 'আদেশ_মোড', 'end': 'শেষ_করা_অফসেট', 'classes': 'শ্রেণী_পথ', 'key': '누름값', 'y': 'Y_বোতাম_অক্ষবিন্দু', 'result': 'পরিমাপ', 'report': 'বৈধকরণ_রিপোর্ট', 'dest': 'গন্তব্য_মান_পদ', 'work': '작업경로', 'qmp': '모의제어접속'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
