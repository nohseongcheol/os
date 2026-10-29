#!/usr/bin/env python3
"""기존 পথ_2 호환 ভুক্তি_বিন্দু. প্রকৃত_ডাটা 구현: ../সরঞ্জামগুলি/바탕화면시험.py"""
import importlib as 가져오기
import sys as অপারেটিং_সিস্টেম_মান
from pathlib import Path as পথ_2
অপারেটিং_সিস্টেম_মান.path.insert(0, str(পথ_2(__file__).resolve().parents[1] / 'সরঞ্জামগুলি'))
if __name__ == '__main__':
    import runpy as অ্যাপ_অ্যাপ_লঞ্চার
    অ্যাপ_অ্যাপ_লঞ্চার.run_module('바탕화면시험', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('바탕화면시험')
    대응 = {'x': 'X_বোতাম_অক্ষবিন্দু', 'typing': '글자입력', 'message': '알림문', 'start': 'চালনা', 'down': '누르는중', 'exact': '정확한값', 'i': '순번', 'press': '글쇠누르기', 'rectangles': '사각형들', 'sym': 'প্রতীক', 'j': '안쪽순번', 'deadline': '마감시각', 'proc': 'প্রসেস', 'data': 'ডাটা', 'main': 'চালনা', 'w': '너비값', 'init': '초기값', 'block': 'ডাটা_আটক_করা', 'ROOT': 'প্রকল্প_মূল', 'text': 'পাঠ', 'marker': '확인표시', 'report': 'বৈধকরণ_রিপোর্ট', 'until': '까지', 'clipboard': 'ক্লিপবোর্ড_মান', 'dst': 'গন্তব্য_ইমেইল', 'seen': '본항목들', 'poll': '준비살피미', 'transcript': '대화기록', 'port': 'পোর্ট_নম্বর', 'offset': 'অফসেট_মান', 'h': '높이값', 'src': '원본주소', 'event': 'ঘটনা', 'encoding': 'অক্ষর_সেট', 'size': 'আকার', 'key': '누름값', 'pixels': '화소들', 'y': 'Y_বোতাম_অক্ষবিন্দু', 'output': '출력결과', 'symbol': 'প্রতীক_মান', 'client': 'গ্রাহক', 'char': 'অক্ষর_ডাটা', 'rgb': '빛삼원색'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
