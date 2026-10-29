#!/usr/bin/env python3
"""기존 මාර්_ගය 호환 පිවිසුම_ලකුණ. තථ්_ය_දත්ත 구현: ../මෙවලම්/바탕화면시험.py"""
import importlib as 가져오기
import sys as මෙහෙයුම්_පද්ධතිය_අගය
from pathlib import Path as මාර්_ගය
මෙහෙයුම්_පද්ධතිය_අගය.path.insert(0, str(මාර්_ගය(__file__).resolve().parents[1] / 'මෙවලම්'))
if __name__ == '__main__':
    import runpy as යෙදු_යෙදුම්_ලාච්චුව
    යෙදු_යෙදුම්_ලාච්චුව.run_module('바탕화면시험', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('바탕화면시험')
    대응 = {'x': 'x_ඛණ්ඩාංකය', 'typing': '글자입력', 'message': '알림문', 'start': 'ක්_රියාත්මක_කරන්න_2', 'down': '누르는중', 'exact': '정확한값', 'i': '순번', 'press': '글쇠누르기', 'rectangles': '사각형들', 'sym': 'සංකේතය', 'j': '안쪽순번', 'deadline': '마감시각', 'proc': 'සැකසුම', 'data': 'දත්ත', 'main': 'ක්_රියාත්මක_කරන්න_2', 'w': '너비값', 'init': '초기값', 'block': 'දත්ත_අවහිර_කරන්න', 'ROOT': '기준', 'text': 'පෙළ', 'marker': '확인표시', 'report': 'වලංගුකරණය_වාර්තාව', 'until': '까지', 'clipboard': 'පසුරු_පුවරුව_අගය', 'dst': 'ගමනාන්තය_යොමුව', 'seen': '본항목들', 'poll': '준비살피미', 'transcript': '대화기록', 'port': '접속번호', 'offset': 'ඕෆ්සෙට්_අගය', 'h': '높이값', 'src': '원본주소', 'event': 'සිදුවීම', 'encoding': 'අනුලකුණු_කුලකය', 'size': 'ප්_රමාණය', 'key': '누름값', 'pixels': '화소들', 'y': '세로좌표', 'output': '출력결과', 'symbol': 'සංකේතය_අගය', 'client': 'සේවාලාභීයා', 'char': 'අනුලකුණ_දත්ත', 'rgb': '빛삼원색'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
