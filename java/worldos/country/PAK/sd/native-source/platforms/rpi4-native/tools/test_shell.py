#!/usr/bin/env python3
"""기존 راههه 호환 داخلا_هنڌ. اصلي_ڪوائف 구현: ../اوزار/셸시험.py"""
import importlib as 가져오기
import sys as آپريٽنگ_سسٽم_قدر
from pathlib import Path as راههه
آپريٽنگ_سسٽم_قدر.path.insert(0, str(راههه(__file__).resolve().parents[1] / 'اوزار'))
if __name__ == '__main__':
    import runpy as ائپ_ائپ_ڊرائر
    ائپ_ائپ_ڊرائر.run_module('셸시험', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('셸시험')
    대응 = {'timeout': '시간제한', 'x': 'x_رطبو', 'msg': 'نيٽ_ورڪ_پيغام', 'i': '순번', 'reply': 'جواب_ڏيو', 'call': '호출', 'args': 'دليل_ترتيب', 'chunk': '조각', 'data': 'ڪوائف', 'proc': 'عمل_a7054519', 'long_text': '긴글', 'restored': '복원자료', 'send': 'اي_ميل', 'file': 'فائل', 'main': 'هلائڻ', 'found': '찾은결과', 'ROOT': '기준', 'text': 'متن', 'marker': '확인표시', 'command': 'حڪم', 'expected': '예상결과', 'pixel': 'پيل', 'shell': 'شيل', 'poll': '준비살피미', 'transcript': '대화기록', 'end': 'ختم_ڪريو_آف_سيٽ', 'image': 'نقش', 'key': '누름값', 'y': '세로좌표', 'output': '출력결과', 'result': '결과', 'client': 'گراهڪ', 'line': 'لڪير', 'stream': 'اسٽريم_قدر', 'name': 'نالو', 'value': 'قدر', 'receive': '수신하기', 'report': 'ڪارگر_رپورٽ', 'work': '작업경로', 'qmp': '모의제어접속'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
