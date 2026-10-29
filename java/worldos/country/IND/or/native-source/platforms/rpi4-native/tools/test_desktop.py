#!/usr/bin/env python3
"""기존 ପଥ 호환 ଏଣ୍ଟ୍ରି_ପଏଣ୍ଟ୍. ପ୍ରକୃତ_ଡାଟା 구현: ../ଉପକରଣସମୂହ/바탕화면시험.py"""
import importlib as 가져오기
import sys as ଅପରେଟିଂ_ସିଷ୍ଟମ_ମୂଲ୍ୟ
from pathlib import Path as ପଥ
ଅପରେଟିଂ_ସିଷ୍ଟମ_ମୂଲ୍ୟ.path.insert(0, str(ପଥ(__file__).resolve().parents[1] / 'ଉପକରଣସମୂହ'))
if __name__ == '__main__':
    import runpy as ଅନୁପ୍ରୟୋଗ_ଆପ୍ଲିକେସନ୍_ଡ୍ରୟର୍
    ଅନୁପ୍ରୟୋଗ_ଆପ୍ଲିକେସନ୍_ଡ୍ରୟର୍.run_module('바탕화면시험', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('바탕화면시험')
    대응 = {'x': 'x_ସଂଯୋଜନ', 'typing': '글자입력', 'message': '알림문', 'start': 'ଚଳାନ୍ତୁ', 'down': '누르는중', 'exact': '정확한값', 'i': '순번', 'press': '글쇠누르기', 'rectangles': '사각형들', 'sym': 'ସଙ୍କେତ', 'j': '안쪽순번', 'deadline': '마감시각', 'proc': 'ପ୍ରକ୍ରିୟା', 'data': 'ଡାଟା', 'main': 'ଚଳାନ୍ତୁ', 'w': '너비값', 'init': '초기값', 'block': 'ଡାଟା_ଅବରୋଧ_କରିବା', 'ROOT': 'ପ୍ରୋଜେକ୍ଟ୍_ରୁଟ୍', 'text': 'ପାଠ୍ଯ', 'marker': '확인표시', 'report': 'ବୈଧକରଣ_ରିପୋର୍ଟ', 'until': '까지', 'clipboard': 'କ୍ଲିପ୍_ବୋର୍ଡ଼_ମୂଲ୍ୟ', 'dst': 'ଲକ୍ଷସ୍ଥଳ_ଠିକଣା', 'seen': '본항목들', 'poll': '준비살피미', 'transcript': '대화기록', 'port': 'ପୋର୍ଟ୍_ନମ୍ଵର୍', 'offset': 'ଅଫ୍_ସେଟ୍_ମୂଲ୍ୟ', 'h': '높이값', 'src': '원본주소', 'event': 'ଘଟଣା', 'encoding': 'ବର୍ଣ୍ଣ_ସେଟ୍', 'size': 'ଆକାର', 'key': '누름값', 'pixels': '화소들', 'y': '세로좌표', 'output': '출력결과', 'symbol': 'ସଙ୍କେତ_ମୂଲ୍ୟ', 'client': 'କ୍ଲାଏଣ୍ଟ', 'char': 'ବର୍ଣ୍ଣ_ଡାଟା', 'rgb': '빛삼원색'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
