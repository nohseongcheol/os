#!/usr/bin/env python3
"""기존 পথ 호환 প্রবিষ্ট_পইণ্ট. প্ৰকৃত_ডাটা 구현: ../সঁজুলিসমূহ/파일전송시험.py"""
import importlib as 가져오기
import sys as অপাৰেটিং_ছিষ্টেম_মান
from pathlib import Path as পথ
অপাৰেটিং_ছিষ্টেম_মান.path.insert(0, str(পথ(__file__).resolve().parents[1] / 'সঁজুলিসমূহ'))
if __name__ == '__main__':
    import runpy as এপ্প্_এপ্প্_ড্ৰৱাৰ
    এপ্প্_এপ্প্_ড্ৰৱাৰ.run_module('파일전송시험', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('파일전송시험')
    대응 = {'timeout': '시간제한', 'payload': 'প্লেল_ড_ডাটা', 'broken': '손상자료', 'linux_example': '리눅스예제', 'chunk': '조각', 'data': 'ডাটা', 'proc': 'প্ৰসেস', 'code': '명령열', 'linux': '리눅스파일', 'archive': 'অভিলেখাগাৰ', 'main': 'সঞ্চালন', 'net_source': '통신원문', 'temporary': '임시자원', 'static_source': 'স্থিৰ_উৎস', 'java_source': '자바원문', 'echo': '되돌림서버항목', 'ROOT': '기준', 'text': 'টেক্সট', 'marker': '확인표시', 'EchoFixture': '되돌림시험서버', 'command': 'কমান্ড', 'out': 'পৰিমাপ_ডাটা', 'expected': '예상결과', 'server_source': 'ছাৰ্ভাৰ_উৎস', 'shell': 'শ্বেল', 'upload': 'আপল_ড_কৰক_ফাইলসমূহ', 'transcript': '대화기록', 'port': '접속번호', 'native': '자체실행파일', 'elf': '실행파일', 'server_udp_port': '서버전문접속번호', 'packed': '묶인자료', 'bridge': 'ব্ৰীজ', 'selector': 'চয়নকাৰী', 'end': 'অন্ত_কৰক_অফছেট', 'e': '보조항목', 'ftp': 'ফাইল_স্থানান্তৰণ_সংযোগ', 'key': '누름값', 'bytecode': '바이트코드', 'peer': 'পীয়েৰ_মান', 'result': 'পৰিমাপ', 'unchanged': '보존자료', 'line': 'লাইন', 'server_tcp_port': 'ছাৰ্ভাৰ_ষ্ট্ৰিম_পৰ্ট', 'source': '원본자료', 'NetworkBridge': 'নেটৱৰ্ক_ব্ৰীজ', 'jar': '자바꾸러미', 'receive': '수신하기', 'report': 'বৈধতা_ৰিপ_ৰ্ট'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
