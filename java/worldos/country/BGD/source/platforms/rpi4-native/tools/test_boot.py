#!/usr/bin/env python3
"""기존 পথ_2 호환 ভুক্তি_বিন্দু. প্রকৃত_ডাটা 구현: ../সরঞ্জামগুলি/부팅시험.py"""
import importlib as 가져오기
import sys as অপারেটিং_সিস্টেম_মান
from pathlib import Path as পথ_2
অপারেটিং_সিস্টেম_মান.path.insert(0, str(পথ_2(__file__).resolve().parents[1] / 'সরঞ্জামগুলি'))
if __name__ == '__main__':
    import runpy as অ্যাপ_অ্যাপ_লঞ্চার
    অ্যাপ_অ্যাপ_লঞ্চার.run_module('부팅시험', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('부팅시험')
    대응 = {'timeout': '시간제한', 'response': '응답자료', 'msg': 'নেটওয়ার্ক_ইমেইল', 'exact': '정확한값', 'markers': '확인표시들', 'i': '순번', 'match': '일치', 'execute': 'চালানো', 'cancel': 'বাতিল_অপারেশন', 'cmd_byte': 'আদেশ_বাইট', 'reply': 'উত্তর_দিন', 'points': '지점들', 'server': 'সার্ভার_মান', 'data': 'ডাটা', 'prompt': 'সত্বর', 'enter': 'প্রবেশ_করা', 'imported': '들여온파일', 'send': 'পাঠান', 'main': 'চালনা', 'ROOT': 'প্রকল্প_মূল', 'text': 'পাঠ', 'first_gui': '첫화면', 'pixel': 'পেল্', 'java_class': '자바클래스', 'upload': 'আপলোড_ফাইলগুলি', 'pixels_file': 'পেল্_ফাইল', 'pixels_data': 'পেল্_ডাটা', 'edit': 'সম্পাদন_মান', 'receive_until': '표시까지받기', 'selector': 'নির্বাচক', 'size': 'আকার', 'qmp_path': '모의제어경로', 'key': '누름값', 'second_gui': '둘째화면', 'y': 'Y_বোতাম_অক্ষবিন্দু', 'result': 'পরিমাপ', 'samples': '예제들', 'client': 'গ্রাহক', 'line': 'নিবেশের_পঙ্_ক্তি', 'report': 'বৈধকরণ_রিপোর্ট', 'work': '작업경로', 'x': 'X_বোতাম_অক্ষবিন্দু', 'python_checks': '파이썬검사', 'download': 'ডাউনলোড', 'greeting': '인사', 'dims': '치수', 'chunk': '조각', 'deadline': '마감시각', 'proc': 'প্রসেস', 'content': 'সামগ্রি_মান', 'block': 'ডাটা_আটক_করা', 'marker': '확인표시', 'command': 'আদেশ', 'expected': '예상결과', 'shell': 'শেল', 'drawing': 'অঙ্কন_পথ', 'f': 'ফাইল_ভুক্তি', 'transcript': '대화기록', 'offset': 'অফসেট_মান', 'path': 'পথ_2', 'screenshot': 'স্ক্রিনশট', 'arguments': '전달인수', 'pixels': '화소들', 'viewer': '화면접속자', 'output': '출력결과', 'stream': 'প্রবাহ_মান', 'cmd': '명령인수', 'name': 'নাম', 'qmp': '모의제어접속'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
