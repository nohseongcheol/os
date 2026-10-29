#!/usr/bin/env python3
"""기존 পথ 호환 প্রবিষ্ট_পইণ্ট. প্ৰকৃত_ডাটা 구현: ../সঁজুলিসমূহ/ডেস্কটপ_দর্শন.py"""
import importlib as 가져오기
import sys as অপাৰেটিং_ছিষ্টেম_মান
from pathlib import Path as পথ
অপাৰেটিং_ছিষ্টেম_মান.path.insert(0, str(পথ(__file__).resolve().parents[1] / 'সঁজুলিসমূহ'))
if __name__ == '__main__':
    import runpy as এপ্প্_এপ্প্_ড্ৰৱাৰ
    এপ্প্_এপ্প্_ড্ৰৱাৰ.run_module('ডেস্কটপ_দর্শন', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('ডেস্কটপ_দর্শন')
    대응 = {'count': '항목수', 'special': '특수글쇠', 'error': 'ত্ৰুটি', 'exact': '정확한값', 'network': 'নেটৱৰ্ক', 'closed': '닫힘', 'length': 'দৈর্ঘ্য_মান', 'opened': '열림', 'ftp_port': '파일전송접속번호', 'server': 'ছাৰ্ভাৰ_মান', 'resources': 'সম্পদসমূহ', 'data': 'ডাটা', 'shift': 'SHIFT_কী', 'send': 'ই_মেইল_কৰক', 'run_desktop': 'চলন_ডেস্কটপ', 'protocol': '통신규약', 'forwards': '전달규칙들', 'host': 'হ_ষ্ট', 'text': 'টেক্সট', 'korean': '한글여부', 'port': '접속번호', 'signum': '신호번호', 'version': '판번호', 'parser': '인수해석기', 'bridge': 'ব্ৰীজ', 'kind': 'বর্গ_মান', 'tail': '끝부분', 'size': 'মাপ', 'previous_buttons': '이전단추', 'key': '누름값', 'y': '세로좌표', 'prefix': '앞부분', 'client': 'ক্লায়েণ্ট', 'char': 'বৰ্ণ_ডাটা', 'work': '작업경로', 'Keyboard': 'কীবোর্ড', 'x': 'x_ক_ৰ্ডিনেট', 'down': '누르는중', 'net': 'নেটৱৰ্ক_ব্ৰীজ_প্রবিষ্ট', 'self': '자신', 'mode_changed': '입력방식알림', 'serial': '직렬입출력', 'args': 'যুক্তি_শৃঙ্খলা', 'Hangul': '한글조합', 'chunk': '조각', 'proc': 'প্ৰসেস', 'Desktop': 'সংযোগ_ডেস্কটপ', 'buttons': '단추들', 'thread': '작업가닥', 'pressed': '눌림', 'previous': '이전항목', 'toggle': 'সাল_সলনি_মোড', 'command': 'কমান্ড', 'sock': '소켓', 'frame': '실행틀', 'ctrl': 'CTRL_কী', 'path': 'পথ', 'cp': 'বৰ্ণ_এনকোডিং', 'terminate': '종료시키기', 'security': 'নিৰাপত্তা', 'vnc_port': '원격화면접속번호', 'body': 'মূল_পাঠ', 'index': 'লুকআপ_ইনডেক্স', 'exited': '종료됨', 'keysym': 'কী_প্ৰতীক', 'output': '출력결과', 'keyboard': 'কীবোর্ড_প্রবিষ্ট', 'interrupted': '가로채기됨', 'listener': '수신창구', 'reader': 'পাঠক', 'NetworkBridge': 'নেটৱৰ্ক_ব্ৰীজ', 'gui': '그림화면', 'worker': '처리작업'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
