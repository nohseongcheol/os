#!/usr/bin/env python3
"""기존 পথ_2 호환 ভুক্তি_বিন্দু. প্রকৃত_ডাটা 구현: ../সরঞ্জামগুলি/파일전송시험.py"""
import importlib as 가져오기
import sys as অপারেটিং_সিস্টেম_মান
from pathlib import Path as পথ_2
অপারেটিং_সিস্টেম_মান.path.insert(0, str(পথ_2(__file__).resolve().parents[1] / 'সরঞ্জামগুলি'))
if __name__ == '__main__':
    import runpy as অ্যাপ_অ্যাপ_লঞ্চার
    অ্যাপ_অ্যাপ_লঞ্চার.run_module('파일전송시험', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('파일전송시험')
    대응 = {'timeout': '시간제한', 'payload': 'পেলোড_ডাটা', 'broken': '손상자료', 'linux_example': '리눅스예제', 'chunk': '조각', 'data': 'ডাটা', 'proc': 'প্রসেস', 'code': '명령열', 'linux': '리눅스파일', 'archive': 'সংগ্রহ_করা', 'main': 'চালনা', 'net_source': '통신원문', 'temporary': '임시자원', 'static_source': 'স্থির_উত্স', 'java_source': '자바원문', 'echo': '되돌림서버항목', 'ROOT': 'প্রকল্প_মূল', 'text': 'পাঠ', 'marker': '확인표시', 'EchoFixture': '되돌림시험서버', 'command': 'আদেশ', 'out': 'পরিমাপ_ডাটা', 'expected': '예상결과', 'server_source': 'সার্ভার_উত্স', 'shell': 'শেল', 'upload': 'আপলোড_ফাইলগুলি', 'transcript': '대화기록', 'port': 'পোর্ট_নম্বর', 'native': '자체실행파일', 'elf': '실행파일', 'server_udp_port': '서버전문접속번호', 'packed': '묶인자료', 'bridge': 'ব্রিজ', 'selector': 'নির্বাচক', 'end': 'শেষ_করা_অফসেট', 'e': '보조항목', 'ftp': 'ফাইল_স্থানান্তর_সংযোগ', 'key': '누름값', 'bytecode': '바이트코드', 'peer': 'পিয়ার_মান', 'result': 'পরিমাপ', 'unchanged': '보존자료', 'line': 'নিবেশের_পঙ্_ক্তি', 'server_tcp_port': 'সার্ভার_প্রবাহ_পোর্ট', 'source': '원본자료', 'NetworkBridge': 'নেটওয়ার্ক_ব্রিজ', 'jar': '자바꾸러미', 'receive': '수신하기', 'report': 'বৈধকরণ_রিপোর্ট'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
