#!/usr/bin/env python3
"""기존 راههه 호환 داخلا_هنڌ. اصلي_ڪوائف 구현: ../اوزار/바탕화면시험.py"""
import importlib as 가져오기
import sys as آپريٽنگ_سسٽم_قدر
from pathlib import Path as راههه
آپريٽنگ_سسٽم_قدر.path.insert(0, str(راههه(__file__).resolve().parents[1] / 'اوزار'))
if __name__ == '__main__':
    import runpy as ائپ_ائپ_ڊرائر
    ائپ_ائپ_ڊرائر.run_module('바탕화면시험', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('바탕화면시험')
    대응 = {'x': 'x_رطبو', 'typing': '글자입력', 'message': '알림문', 'start': 'هلائڻ', 'down': '누르는중', 'exact': '정확한값', 'i': '순번', 'press': '글쇠누르기', 'rectangles': '사각형들', 'sym': 'نشاني', 'j': '안쪽순번', 'deadline': '마감시각', 'proc': 'عمل_a7054519', 'data': 'ڪوائف', 'main': 'هلائڻ', 'w': '너비값', 'init': '초기값', 'block': 'ڪوائف_بلاڪ_ڪريو', 'ROOT': '기준', 'text': 'متن', 'marker': '확인표시', 'report': 'ڪارگر_رپورٽ', 'until': '까지', 'clipboard': 'تراشه_تختو_قدر', 'dst': 'منزل_مقصود_پتو', 'seen': '본항목들', 'poll': '준비살피미', 'transcript': '대화기록', 'port': '접속번호', 'offset': 'آف_سيٽ_قدر', 'h': '높이값', 'src': '원본주소', 'event': 'واقعو', 'encoding': 'ڪيريڪٽرن_جو_سيٽ', 'size': 'سائيز', 'key': '누름값', 'pixels': '화소들', 'y': '세로좌표', 'output': '출력결과', 'symbol': 'نشاني_قدر', 'client': 'گراهڪ', 'char': 'ڪريڪٽر_ڪوائف', 'rgb': '빛삼원색'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
