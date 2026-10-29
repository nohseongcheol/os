#!/usr/bin/env python3
"""기존 পথ 호환 প্রবিষ্ট_পইণ্ট. প্ৰকৃত_ডাটা 구현: ../সঁজুলিসমূহ/화면요소시험.py"""
import importlib as 가져오기
import sys as অপাৰেটিং_ছিষ্টেম_মান
from pathlib import Path as পথ
অপাৰেটিং_ছিষ্টেম_মান.path.insert(0, str(পথ(__file__).resolve().parents[1] / 'সঁজুলিসমূহ'))
if __name__ == '__main__':
    import runpy as এপ্প্_এপ্প্_ড্ৰৱাৰ
    এপ্প্_এপ্প্_ড্ৰৱাৰ.run_module('화면요소시험', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('화면요소시험')
    대응 = {'wait': '기다리기', 'x': 'x_ক_ৰ্ডিনেট', 's': 'ষ্ট্ৰিং_ডাটা', 'i': '순번', 'sel': 'চয়নকাৰী_a916db4e', 'seconds': '초단위', 'log': 'লগ_শাৰী', 'data': 'ডাটা', 'at': '현재위치', 'send': 'ই_মেইল_কৰক', 'main': 'সঞ্চালন', 'req': '요청값', 'hot': 'চমুপথ_মান', 'pump': 'হেণ্ডেল_ইভেণ্ট', 'ROOT': '기준', 'marker': '확인표시', 'b': '둘째값', 'command': 'কমান্ড', 'shell': 'শ্বেল', 'f': 'ফাইল_প্রবিষ্ট', 'click': 'ক্লিক_কৰক_বুটাম', 'k': '셋째순번', 'c': 'বৰ্ণ_ক_ড', 'r': '반환값', 'p': 'ডাটা_স্থান_সলনি_কৰক', 'command_mode': 'আদেশ_মোড', 'end': 'অন্ত_কৰক_অফছেট', 'classes': 'শ্ৰেণী_পথ', 'key': '누름값', 'y': '세로좌표', 'result': 'পৰিমাপ', 'report': 'বৈধতা_ৰিপ_ৰ্ট', 'dest': 'গন্তব্য_স্থান_মান_স্থান_সলনি_কৰক', 'work': '작업경로', 'qmp': '모의제어접속'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
