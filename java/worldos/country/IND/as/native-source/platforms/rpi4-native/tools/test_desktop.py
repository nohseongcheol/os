#!/usr/bin/env python3
"""기존 পথ 호환 প্রবিষ্ট_পইণ্ট. প্ৰকৃত_ডাটা 구현: ../সঁজুলিসমূহ/바탕화면시험.py"""
import importlib as 가져오기
import sys as অপাৰেটিং_ছিষ্টেম_মান
from pathlib import Path as পথ
অপাৰেটিং_ছিষ্টেম_মান.path.insert(0, str(পথ(__file__).resolve().parents[1] / 'সঁজুলিসমূহ'))
if __name__ == '__main__':
    import runpy as এপ্প্_এপ্প্_ড্ৰৱাৰ
    এপ্প্_এপ্প্_ড্ৰৱাৰ.run_module('바탕화면시험', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('바탕화면시험')
    대응 = {'x': 'x_ক_ৰ্ডিনেট', 'typing': '글자입력', 'message': '알림문', 'start': 'সঞ্চালন', 'down': '누르는중', 'exact': '정확한값', 'i': '순번', 'press': '글쇠누르기', 'rectangles': '사각형들', 'sym': 'প্ৰতীক', 'j': '안쪽순번', 'deadline': '마감시각', 'proc': 'প্ৰসেস', 'data': 'ডাটা', 'main': 'সঞ্চালন', 'w': '너비값', 'init': '초기값', 'block': 'ডাটা_অৱৰুদ্ধ_কৰক', 'ROOT': '기준', 'text': 'টেক্সট', 'marker': '확인표시', 'report': 'বৈধতা_ৰিপ_ৰ্ট', 'until': '까지', 'clipboard': 'ক্লিপ_বোৰ্ড_মান', 'dst': 'গন্তব্য_স্থান_ঠিকনা', 'seen': '본항목들', 'poll': '준비살피미', 'transcript': '대화기록', 'port': '접속번호', 'offset': 'অফছেট_মান', 'h': '높이값', 'src': '원본주소', 'event': 'ইভেণ্ট', 'encoding': 'বৰ্ণ_ছেট', 'size': 'মাপ', 'key': '누름값', 'pixels': '화소들', 'y': '세로좌표', 'output': '출력결과', 'symbol': 'প্ৰতীক_মান', 'client': 'ক্লায়েণ্ট', 'char': 'বৰ্ণ_ডাটা', 'rgb': '빛삼원색'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
