#!/usr/bin/env python3
"""기존 পথ 호환 প্রবিষ্ট_পইণ্ট. প্ৰকৃত_ডাটা 구현: ../সঁজুলিসমূহ/নেটৱৰ্ক_ব্ৰীজ.py"""
import importlib as 가져오기
import sys as অপাৰেটিং_ছিষ্টেম_মান
from pathlib import Path as পথ
অপাৰেটিং_ছিষ্টেম_মান.path.insert(0, str(পথ(__file__).resolve().parents[1] / 'সঁজুলিসমূহ'))
if __name__ == '__main__':
    import runpy as এপ্প্_এপ্প্_ড্ৰৱাৰ
    এপ্প্_এপ্প্_ড্ৰৱাৰ.run_module('নেটৱৰ্ক_ব্ৰীজ', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('নেটৱৰ্ক_ব্ৰীজ')
    대응 = {'response': '응답자료', 'parts': 'পথ_উপাদান', 's': 'ষ্ট্ৰিং_ডাটা', 'i': '순번', 'close': 'বন্ধ_কৰক', 'forward': '전달규칙', 'slip_input': '직렬전문입력', 'self': '자신', 'item': 'প্রবিষ্ট_মান', 'flags': '설정비트', 'ftp_port': '파일전송접속번호', 'args': 'যুক্তি_শৃঙ্খলা', 'server': 'ছাৰ্ভাৰ_মান', 'data': 'ডাটা', 'ethernet_input': '이더넷입력', 'trace_packet': 'ট্ৰেচ_পেকেট', 'GATEWAY': '관문기계주소', 'rule': 'নীতি_মান', 'protocol': '통신규약', 'forwards': '전달규칙들', 'occupied': '사용중주소', 'host': 'হ_ষ্ট', 'ack': '확인번호', 'serial_port': '직렬접속번호', 'readers': '읽기대상들', 'guest': 'অতিথি', 'destination': 'গন্তব্য_স্থান_ডাটা_ঠিকনা', 'ethernet_port': 'ইথাৰনেট_পৰ্ট', 'b': '둘째값', 'MAC': 'মেচিন_ঠিকনা', 'arp': 'ঠিকনা_প্রতিচ্ছায়া_পেকেট', 'writable': '쓸수있음', 'direction': '방향', 'seq': '순서번호', 'frame': '실행틀', 'loop': 'চক্ৰ_মান', 'port': '접속번호', 'offset': 'অফছেট_মান', 'readable': '읽을수있음', 'c': 'বৰ্ণ_ক_ড', 'p': 'ডাটা_স্থান_সলনি_কৰক', 'writers': '쓰기대상들', 'IP': 'ইন্টাৰনেট_ঠিকনা_মান', 'e': '보조항목', 'n': '개수', 'packet': 'পেকেট_ডাটা', 'arguments': '전달인수', 'source': '원본자료', 'NetworkBridge': 'নেটৱৰ্ক_ব্ৰীজ', 'window': 'উইণ্ড', 'capture': 'কেপচাৰ'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
