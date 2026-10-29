#!/usr/bin/env python3
"""기존 يونلور 호환 ننوت_ټکى. 실제 구현: ../도구/바탕화면시험.py"""
import importlib as 가져오기
import sys as چليز_غونډال_ارزښت
from pathlib import Path as يونلور
چليز_غونډال_ارزښت.path.insert(0, str(يونلور(__file__).resolve().parents[1] / '도구'))
if __name__ == '__main__':
    import runpy as 실행기
    실행기.run_module('바탕화면시험', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('바탕화면시험')
    대응 = {'x': '가로좌표', 'typing': '글자입력', 'message': '알림문', 'start': 'ځغلول', 'down': '누르는중', 'exact': '정확한값', 'i': '순번', 'press': '글쇠누르기', 'rectangles': '사각형들', 'sym': '기호', 'j': '안쪽순번', 'deadline': '마감시각', 'proc': 'بهير', 'data': 'اومتوک', 'main': 'ځغلول', 'w': '너비값', 'init': '초기값', 'block': '자료덩이', 'ROOT': '기준', 'text': 'ليکنه', 'marker': '확인표시', 'report': 'باورکړن_راپور', 'until': '까지', 'clipboard': 'ټوټه_دړه_ارزښت', 'dst': 'موخه_پته', 'seen': '본항목들', 'poll': '준비살피미', 'transcript': '대화기록', 'port': '접속번호', 'offset': '변위', 'h': '높이값', 'src': '원본주소', 'event': 'پېښه', 'encoding': 'لوښه_غونډ', 'size': 'کچ', 'key': '누름값', 'pixels': '화소들', 'y': '세로좌표', 'output': '출력결과', 'symbol': '심볼', 'client': 'پېرن', 'char': 'لوښه_اومتوک', 'rgb': '빛삼원색'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
