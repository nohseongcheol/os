#!/usr/bin/env python3
"""기존 পথ 호환 প্রবিষ্ট_পইণ্ট. প্ৰকৃত_ডাটা 구현: ../সঁজুলিসমূহ/셸시험.py"""
import importlib as 가져오기
import sys as অপাৰেটিং_ছিষ্টেম_মান
from pathlib import Path as পথ
অপাৰেটিং_ছিষ্টেম_মান.path.insert(0, str(পথ(__file__).resolve().parents[1] / 'সঁজুলিসমূহ'))
if __name__ == '__main__':
    import runpy as এপ্প্_এপ্প্_ড্ৰৱাৰ
    এপ্প্_এপ্প্_ড্ৰৱাৰ.run_module('셸시험', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('셸시험')
    대응 = {'timeout': '시간제한', 'x': 'x_ক_ৰ্ডিনেট', 'msg': 'নেটৱৰ্ক_বাৰ্তা', 'i': '순번', 'reply': 'প্ৰত্যুত্তৰ_দিয়ক', 'call': '호출', 'args': 'যুক্তি_শৃঙ্খলা', 'chunk': '조각', 'data': 'ডাটা', 'proc': 'প্ৰসেস', 'long_text': '긴글', 'restored': '복원자료', 'send': 'ই_মেইল_কৰক', 'file': 'নথিপত্ৰ', 'main': 'সঞ্চালন', 'found': 'অনুসন্ধান_পৰিমাপ', 'ROOT': '기준', 'text': 'টেক্সট', 'marker': '확인표시', 'command': 'কমান্ড', 'expected': '예상결과', 'pixel': 'পিক্সেল', 'shell': 'শ্বেল', 'poll': '준비살피미', 'transcript': '대화기록', 'end': 'অন্ত_কৰক_অফছেট', 'image': 'ছবি', 'key': '누름값', 'y': '세로좌표', 'output': '출력결과', 'result': 'পৰিমাপ', 'client': 'ক্লায়েণ্ট', 'line': 'লাইন', 'stream': 'ষ্ট্ৰিম_মান', 'name': 'নাম', 'value': 'মান', 'receive': '수신하기', 'report': 'বৈধতা_ৰিপ_ৰ্ট', 'work': '작업경로', 'qmp': '모의제어접속'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
