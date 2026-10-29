#!/usr/bin/env python3
"""기존 পথ_2 호환 ভুক্তি_বিন্দু. প্রকৃত_ডাটা 구현: ../সরঞ্জামগুলি/예제시험.py"""
import importlib as 가져오기
import sys as অপারেটিং_সিস্টেম_মান
from pathlib import Path as পথ_2
অপারেটিং_সিস্টেম_মান.path.insert(0, str(পথ_2(__file__).resolve().parents[1] / 'সরঞ্জামগুলি'))
if __name__ == '__main__':
    import runpy as অ্যাপ_অ্যাপ_লঞ্চার
    অ্যাপ_অ্যাপ_লঞ্চার.run_module('예제시험', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('예제시험')
    대응 = {'count': '항목수', 'exact': '정확한값', 'expected_file': '예상파일', 'ftp_port': 'ফাইল_স্থানান্তর_পোর্ট_নম্বর', 'data': 'ডাটা', 'graphics_command': 'গ্রাফিক্স_আদেশ', 'main': 'চালনা', 'row': 'সারি_পদ', 'init': '초기값', 'target': 'লক্ষ্য', 'ROOT': 'প্রকল্প_মূল', 'text': 'পাঠ', 'binary': 'বাইনারি', 'out': 'পরিমাপ_ডাটা', 'entry': 'ভুক্তি_বিন্দু', 'got': '받은수', 'port': 'পোর্ট_নম্বর', 'graphics_start': 'শুরু_অঙ্কন', 'col': 'কলাম_পদ', 'begin': 'শুরু_অফসেট', 'kind': 'বিভাগ_মান', 'selector': 'নির্বাচক', 'n': '개수', 'key': '누름값', 'y': 'Y_বোতাম_অক্ষবিন্দু', 'client': 'গ্রাহক', 'line': 'নিবেশের_পঙ্_ক্তি', 'report': 'বৈধকরণ_রিপোর্ট', 'language': 'ভাষা', 'x': 'X_বোতাম_অক্ষবিন্দু', 'start': 'চালনা', 'rgb': '빛삼원색', 'down': '누르는중', 'listing': 'পাঠান_তালিকা', 'payload': 'পেলোড_ডাটা', 'proc': 'প্রসেস', 'w': '너비값', 'temporary': '임시자원', 'echo': '되돌림서버항목', 'label': 'নাম_সারণি', 'content': 'সামগ্রি_মান', 'argument': '전달값', 'EchoServers': '되돌림서버', 'marker': '확인표시', 'expected': '예상결과', 'test_language': 'test_언어', 'filename': 'ফাইল_ভুক্তি_নাম', 'shell': 'শেল', 'color': '색상', 'transcript': '대화기록', 'offset': 'অফসেট_মান', 'h': '높이값', 'run': 'কার্যকর_করুন_আদেশ', 'c': 'অক্ষর_কোড', 'path': 'পথ_2', 'encoding': 'অক্ষর_সেট', 'end': 'শেষ_করা_অফসেট', 'ftp': 'ফাইল_স্থানান্তর_সংযোগ', 'pixels': '화소들', 'symbol': 'প্রতীক_মান', 'source': '원본자료', 'name': 'নাম', 'receive': '수신하기', 'manifest': '꾸러미명세'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
