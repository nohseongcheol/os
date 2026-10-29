#!/usr/bin/env python3
"""기존 পথ 호환 প্রবিষ্ট_পইণ্ট. প্ৰকৃত_ডাটা 구현: ../সঁজুলিসমূহ/원격한글시험.py"""
import importlib as 가져오기
import sys as অপাৰেটিং_ছিষ্টেম_মান
from pathlib import Path as পথ
অপাৰেটিং_ছিষ্টেম_মান.path.insert(0, str(পথ(__file__).resolve().parents[1] / 'সঁজুলিসমূহ'))
if __name__ == '__main__':
    import runpy as এপ্প্_এপ্প্_ড্ৰৱাৰ
    এপ্প্_এপ্প্_ড্ৰৱাৰ.run_module('원격한글시험', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('원격한글시험')
    대응 = {'wait': '기다리기', 'typing': '글자입력', 'start': 'সঞ্চালন', 'profile': 'প্ৰ_ফাইল', 'focused': 'দৃষ্টি_নিবদ্ধ', 'serial': '직렬입출력', 'keys': '누름열', 'server': 'ছাৰ্ভাৰ_মান', 'log': 'লগ_শাৰী', 'args': 'যুক্তি_শৃঙ্খলা', 'deadline': '마감시각', 'data': 'ডাটা', 'candidate': '후보', 'logs': '기록들', 'kw': '이름붙인인수', 'number': '수치', 'main': 'সঞ্চালন', 'ready': '준비완료', 'found': 'অনুসন্ধান_পৰিমাপ', 'guest': 'অতিথি', 'ROOT': '기준', 'marker': '확인표시', 'text': 'টেক্সট', 'out': 'পৰিমাপ_ডাটা', 'env': '환경', 'f': 'ফাইল_প্রবিষ্ট', 'port': '접속번호', 'offset': 'অফছেট_মান', 'version': '판번호', 'p': 'ডাটা_স্থান_সলনি_কৰক', 'selector': 'চয়নকাৰী', 'xvfb': 'ভাৰ্ছুৱেল_প্রদর্শন', 'display': 'প্রদর্শন', 'n': '개수', 'key': '누름값', 'processes': '실행과정들', 'rootfs': '뿌리파일계층', 'xdo': '가상입력도구', 'name': 'নাম', 'window': 'উইণ্ড', 'report': 'বৈধতা_ৰিপ_ৰ্ট', 'work': '작업경로'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
