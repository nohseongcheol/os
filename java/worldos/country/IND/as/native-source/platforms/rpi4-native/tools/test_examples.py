#!/usr/bin/env python3
"""기존 পথ 호환 প্রবিষ্ট_পইণ্ট. প্ৰকৃত_ডাটা 구현: ../সঁজুলিসমূহ/예제시험.py"""
import importlib as 가져오기
import sys as অপাৰেটিং_ছিষ্টেম_মান
from pathlib import Path as পথ
অপাৰেটিং_ছিষ্টেম_মান.path.insert(0, str(পথ(__file__).resolve().parents[1] / 'সঁজুলিসমূহ'))
if __name__ == '__main__':
    import runpy as এপ্প্_এপ্প্_ড্ৰৱাৰ
    এপ্প্_এপ্প্_ড্ৰৱাৰ.run_module('예제시험', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('예제시험')
    대응 = {'count': '항목수', 'exact': '정확한값', 'expected_file': '예상파일', 'ftp_port': '파일전송접속번호', 'data': 'ডাটা', 'graphics_command': 'গ্ৰাফিক্স_আদেশ', 'main': 'সঞ্চালন', 'row': 'শাৰী_স্থান_সলনি_কৰক', 'init': '초기값', 'target': 'লক্ষ্য', 'ROOT': '기준', 'text': 'টেক্সট', 'binary': 'বাইনেৰি', 'out': 'পৰিমাপ_ডাটা', 'entry': 'প্রবিষ্ট_পইণ্ট', 'got': '받은수', 'port': '접속번호', 'graphics_start': 'আৰম্ভ_অংকন', 'col': 'স্তম্ভ_স্থান_সলনি_কৰক', 'begin': 'আৰম্ভ_অফছেট', 'kind': 'বর্গ_মান', 'selector': 'চয়নকাৰী', 'n': '개수', 'key': '누름값', 'y': '세로좌표', 'client': 'ক্লায়েণ্ট', 'line': 'লাইন', 'report': 'বৈধতা_ৰিপ_ৰ্ট', 'language': 'ভাষা', 'x': 'x_ক_ৰ্ডিনেট', 'start': 'সঞ্চালন', 'rgb': '빛삼원색', 'down': '누르는중', 'listing': 'ই_মেইল_কৰক_সূচী', 'payload': 'প্লেল_ড_ডাটা', 'proc': 'প্ৰসেস', 'w': '너비값', 'temporary': '임시자원', 'echo': '되돌림서버항목', 'label': 'নাম_তালিকা', 'content': 'সামগ্ৰী_মান', 'argument': '전달값', 'EchoServers': '되돌림서버', 'marker': '확인표시', 'expected': '예상결과', 'test_language': 'test_언어', 'filename': 'ফাইল_প্রবিষ্ট_নাম', 'shell': 'শ্বেল', 'color': '색상', 'transcript': '대화기록', 'offset': 'অফছেট_মান', 'h': '높이값', 'run': 'নিষ্পাদন_আদেশ', 'c': 'বৰ্ণ_ক_ড', 'path': 'পথ', 'encoding': 'বৰ্ণ_ছেট', 'end': 'অন্ত_কৰক_অফছেট', 'ftp': 'ফাইল_স্থানান্তৰণ_সংযোগ', 'pixels': '화소들', 'symbol': 'প্ৰতীক_মান', 'source': '원본자료', 'name': 'নাম', 'receive': '수신하기', 'manifest': '꾸러미명세'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
