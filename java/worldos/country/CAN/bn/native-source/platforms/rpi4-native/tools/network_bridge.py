#!/usr/bin/env python3
"""기존 পথ_2 호환 ভুক্তি_বিন্দু. প্রকৃত_ডাটা 구현: ../সরঞ্জামগুলি/নেটওয়ার্ক_ব্রিজ.py"""
import importlib as 가져오기
import sys as অপারেটিং_সিস্টেম_মান
from pathlib import Path as পথ_2
অপারেটিং_সিস্টেম_মান.path.insert(0, str(পথ_2(__file__).resolve().parents[1] / 'সরঞ্জামগুলি'))
if __name__ == '__main__':
    import runpy as অ্যাপ_অ্যাপ_লঞ্চার
    অ্যাপ_অ্যাপ_লঞ্চার.run_module('নেটওয়ার্ক_ব্রিজ', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('নেটওয়ার্ক_ব্রিজ')
    대응 = {'response': '응답자료', 'parts': 'পথ_অঙ্গ', 's': 'স্ট্রিং_ডাটা', 'i': '순번', 'close': 'বন্ধ_করুন', 'forward': '전달규칙', 'slip_input': '직렬전문입력', 'self': '자신', 'item': 'ভুক্তি_মান', 'flags': 'বিন্যাসন_ব্যাকগ্রাউন্ড_ইনটেলিজেন্ট_ট্র্যান্সফার_সার্ভিস', 'ftp_port': 'ফাইল_স্থানান্তর_পোর্ট_নম্বর', 'args': 'যুক্তি_অ্যারে', 'server': 'সার্ভার_মান', 'data': 'ডাটা', 'ethernet_input': '이더넷입력', 'trace_packet': 'ট্রেস_প্যাকেট', 'GATEWAY': 'গেটওয়ে_হার্ডওয়্যার_ইমেইল', 'rule': 'নিয়ম_মান', 'protocol': '통신규약', 'forwards': '전달규칙들', 'occupied': '사용중주소', 'host': 'হোস্ট', 'ack': '확인번호', 'serial_port': '직렬접속번호', 'readers': '읽기대상들', 'guest': 'অতিথি', 'destination': 'গন্তব্য_ডাটা_ইমেইল', 'ethernet_port': 'ইথারনেট_পোর্ট', 'b': '둘째값', 'MAC': 'মেশিন_ইমেইল', 'arp': 'ইমেইল_রেজোলিউশন_প্যাকেট', 'writable': '쓸수있음', 'direction': '방향', 'seq': '순서번호', 'frame': '실행틀', 'loop': 'চক্র_মান', 'port': 'পোর্ট_নম্বর', 'offset': 'অফসেট_মান', 'readable': '읽을수있음', 'c': 'অক্ষর_কোড', 'p': 'ডাটা_পদ', 'writers': '쓰기대상들', 'IP': 'ইন্টারনেট_ঠিকানা_মান', 'e': '보조항목', 'n': '개수', 'packet': 'প্যাকেট_ডাটা', 'arguments': '전달인수', 'source': '원본자료', 'NetworkBridge': 'নেটওয়ার্ক_ব্রিজ', 'window': 'উইন্ডো', 'capture': 'ক্যাপচার'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
