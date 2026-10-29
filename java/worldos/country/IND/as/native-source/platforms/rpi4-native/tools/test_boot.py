#!/usr/bin/env python3
"""기존 পথ 호환 প্রবিষ্ট_পইণ্ট. প্ৰকৃত_ডাটা 구현: ../সঁজুলিসমূহ/부팅시험.py"""
import importlib as 가져오기
import sys as অপাৰেটিং_ছিষ্টেম_মান
from pathlib import Path as পথ
অপাৰেটিং_ছিষ্টেম_মান.path.insert(0, str(পথ(__file__).resolve().parents[1] / 'সঁজুলিসমূহ'))
if __name__ == '__main__':
    import runpy as এপ্প্_এপ্প্_ড্ৰৱাৰ
    এপ্প্_এপ্প্_ড্ৰৱাৰ.run_module('부팅시험', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('부팅시험')
    대응 = {'timeout': '시간제한', 'response': '응답자료', 'msg': 'নেটৱৰ্ক_বাৰ্তা', 'exact': '정확한값', 'markers': '확인표시들', 'i': '순번', 'match': '일치', 'execute': 'চলাওক', 'cancel': 'বাতিল_কৰক_অপাৰেচন', 'cmd_byte': 'আদেশ_বাইট', 'reply': 'প্ৰত্যুত্তৰ_দিয়ক', 'points': '지점들', 'server': 'ছাৰ্ভাৰ_মান', 'data': 'ডাটা', 'prompt': 'সংকেত', 'enter': 'প্ৰৱেশ_কৰক', 'imported': '들여온파일', 'send': 'ই_মেইল_কৰক', 'main': 'সঞ্চালন', 'ROOT': '기준', 'text': 'টেক্সট', 'first_gui': '첫화면', 'pixel': 'পিক্সেল', 'java_class': '자바클래스', 'upload': 'আপল_ড_কৰক_ফাইলসমূহ', 'pixels_file': 'পিক্সেল_ফাইল', 'pixels_data': 'পিক্সেল_ডাটা', 'edit': 'সম্পাদনা_মান', 'receive_until': '표시까지받기', 'selector': 'চয়নকাৰী', 'size': 'মাপ', 'qmp_path': '모의제어경로', 'key': '누름값', 'second_gui': '둘째화면', 'y': '세로좌표', 'result': 'পৰিমাপ', 'samples': '예제들', 'client': 'ক্লায়েণ্ট', 'line': 'লাইন', 'report': 'বৈধতা_ৰিপ_ৰ্ট', 'work': '작업경로', 'x': 'x_ক_ৰ্ডিনেট', 'python_checks': '파이썬검사', 'download': 'ডাউনলোড', 'greeting': '인사', 'dims': '치수', 'chunk': '조각', 'deadline': '마감시각', 'proc': 'প্ৰসেস', 'content': 'সামগ্ৰী_মান', 'block': 'ডাটা_অৱৰুদ্ধ_কৰক', 'marker': '확인표시', 'command': 'কমান্ড', 'expected': '예상결과', 'shell': 'শ্বেল', 'drawing': 'অংকন_পথ', 'f': 'ফাইল_প্রবিষ্ট', 'transcript': '대화기록', 'offset': 'অফছেট_মান', 'path': 'পথ', 'screenshot': 'স্ক্ৰীণ_ক্লিপিং', 'arguments': '전달인수', 'pixels': '화소들', 'viewer': '화면접속자', 'output': '출력결과', 'stream': 'ষ্ট্ৰিম_মান', 'cmd': '명령인수', 'name': 'নাম', 'qmp': '모의제어접속'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
