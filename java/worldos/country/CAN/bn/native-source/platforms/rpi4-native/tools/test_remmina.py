#!/usr/bin/env python3
"""기존 পথ_2 호환 ভুক্তি_বিন্দু. প্রকৃত_ডাটা 구현: ../সরঞ্জামগুলি/원격한글시험.py"""
import importlib as 가져오기
import sys as অপারেটিং_সিস্টেম_মান
from pathlib import Path as পথ_2
অপারেটিং_সিস্টেম_মান.path.insert(0, str(পথ_2(__file__).resolve().parents[1] / 'সরঞ্জামগুলি'))
if __name__ == '__main__':
    import runpy as অ্যাপ_অ্যাপ_লঞ্চার
    অ্যাপ_অ্যাপ_লঞ্চার.run_module('원격한글시험', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('원격한글시험')
    대응 = {'wait': '기다리기', 'typing': '글자입력', 'start': 'চালনা', 'profile': 'বিবরণী', 'focused': 'ফোকাসযুক্ত', 'serial': '직렬입출력', 'keys': '누름열', 'server': 'সার্ভার_মান', 'log': 'লগ_সারি', 'args': 'যুক্তি_অ্যারে', 'deadline': '마감시각', 'data': 'ডাটা', 'candidate': '후보', 'logs': '기록들', 'kw': '이름붙인인수', 'number': '수치', 'main': 'চালনা', 'ready': '준비완료', 'found': 'দেখুন_পরিমাপ', 'guest': 'অতিথি', 'ROOT': 'প্রকল্প_মূল', 'marker': '확인표시', 'text': 'পাঠ', 'out': 'পরিমাপ_ডাটা', 'env': '환경', 'f': 'ফাইল_ভুক্তি', 'port': 'পোর্ট_নম্বর', 'offset': 'অফসেট_মান', 'version': '판번호', 'p': 'ডাটা_পদ', 'selector': 'নির্বাচক', 'xvfb': 'কল্পিত_ডিসপ্লে', 'display': 'ডিসপ্লে', 'n': '개수', 'key': '누름값', 'processes': '실행과정들', 'rootfs': '뿌리파일계층', 'xdo': '가상입력도구', 'name': 'নাম', 'window': 'উইন্ডো', 'report': 'বৈধকরণ_রিপোর্ট', 'work': '작업경로'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
