#!/usr/bin/env python3
"""기존 পথ_2 호환 ভুক্তি_বিন্দু. প্রকৃত_ডাটা 구현: ../সরঞ্জামগুলি/ডেস্কটপ_ভিউ.py"""
import importlib as 가져오기
import sys as অপারেটিং_সিস্টেম_মান
from pathlib import Path as পথ_2
অপারেটিং_সিস্টেম_মান.path.insert(0, str(পথ_2(__file__).resolve().parents[1] / 'সরঞ্জামগুলি'))
if __name__ == '__main__':
    import runpy as অ্যাপ_অ্যাপ_লঞ্চার
    অ্যাপ_অ্যাপ_লঞ্চার.run_module('ডেস্কটপ_ভিউ', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('ডেস্কটপ_ভিউ')
    대응 = {'count': '항목수', 'special': '특수글쇠', 'error': 'ত্রুটি', 'exact': '정확한값', 'network': 'নেটওয়ার্ক_9b2e3222', 'closed': '닫힘', 'length': 'দৈর্ঘ্য_মান', 'opened': '열림', 'ftp_port': 'ফাইল_স্থানান্তর_পোর্ট_নম্বর', 'server': 'সার্ভার_মান', 'resources': 'সম্পদগুলি', 'data': 'ডাটা', 'shift': 'SHIFT_কী', 'send': 'পাঠান', 'run_desktop': 'রান_ডেস্কটপ', 'protocol': '통신규약', 'forwards': '전달규칙들', 'host': 'হোস্ট', 'text': 'পাঠ', 'korean': '한글여부', 'port': 'পোর্ট_নম্বর', 'signum': '신호번호', 'version': '판번호', 'parser': 'পার্সার', 'bridge': 'ব্রিজ', 'kind': 'বিভাগ_মান', 'tail': '끝부분', 'size': 'আকার', 'previous_buttons': '이전단추', 'key': '누름값', 'y': 'Y_বোতাম_অক্ষবিন্দু', 'prefix': '앞부분', 'client': 'গ্রাহক', 'char': 'অক্ষর_ডাটা', 'work': '작업경로', 'Keyboard': 'কীবোর্ড', 'x': 'X_বোতাম_অক্ষবিন্দু', 'down': '누르는중', 'net': 'নেটওয়ার্ক_ব্রিজ_ভুক্তি', 'self': '자신', 'mode_changed': '입력방식알림', 'serial': '직렬입출력', 'args': 'যুক্তি_অ্যারে', 'Hangul': '한글조합', 'chunk': '조각', 'proc': 'প্রসেস', 'Desktop': 'সংযোগ_ডেস্কটপ', 'buttons': '단추들', 'thread': '작업가닥', 'pressed': '눌림', 'previous': '이전항목', 'toggle': 'সুইচ_মোড', 'command': 'আদেশ', 'sock': '소켓', 'frame': '실행틀', 'ctrl': 'CTRL_কী', 'path': 'পথ_2', 'cp': 'অক্ষর_এনকোড_করা', 'terminate': '종료시키기', 'security': 'নিরাপত্তা', 'vnc_port': '원격화면접속번호', 'body': 'মুখ্য_পাঠ', 'index': 'লুকআপ_সূচি', 'exited': '종료됨', 'keysym': 'কী_প্রতীক', 'output': '출력결과', 'keyboard': 'কীবোর্ড_ভুক্তি', 'interrupted': '가로채기됨', 'listener': '수신창구', 'reader': 'পাঠক', 'NetworkBridge': 'নেটওয়ার্ক_ব্রিজ', 'gui': '그림화면', 'worker': '처리작업'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
