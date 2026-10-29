#!/usr/bin/env python3
"""기존 මාර්_ගය 호환 පිවිසුම_ලකුණ. තථ්_ය_දත්ත 구현: ../මෙවලම්/셸시험.py"""
import importlib as 가져오기
import sys as මෙහෙයුම්_පද්ධතිය_අගය
from pathlib import Path as මාර්_ගය
මෙහෙයුම්_පද්ධතිය_අගය.path.insert(0, str(මාර්_ගය(__file__).resolve().parents[1] / 'මෙවලම්'))
if __name__ == '__main__':
    import runpy as යෙදු_යෙදුම්_ලාච්චුව
    යෙදු_යෙදුම්_ලාච්චුව.run_module('셸시험', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('셸시험')
    대응 = {'timeout': '시간제한', 'x': 'x_ඛණ්ඩාංකය', 'msg': 'ජාලය_පණිවිඩය', 'i': '순번', 'reply': 'පිළිතුරු_දෙන්න', 'call': '호출', 'args': 'විස්තාරකය_ආරා_ව', 'chunk': '조각', 'data': 'දත්ත', 'proc': 'සැකසුම', 'long_text': '긴글', 'restored': '복원자료', 'send': 'ඊමේල්', 'file': 'ගොනු', 'main': 'ක්_රියාත්මක_කරන්න_2', 'found': '찾은결과', 'ROOT': '기준', 'text': 'පෙළ', 'marker': '확인표시', 'command': 'විධානය', 'expected': '예상결과', 'pixel': 'පික්සලය', 'shell': 'කවචය', 'poll': '준비살피미', 'transcript': '대화기록', 'end': 'නිමා_කරන්න_ඕෆ්සෙට්', 'image': 'අනුරුව', 'key': '누름값', 'y': '세로좌표', 'output': '출력결과', 'result': '결과', 'client': 'සේවාලාභීයා', 'line': 'පේළිය', 'stream': 'දහර_අගය', 'name': 'නම', 'value': 'අගය', 'receive': '수신하기', 'report': 'වලංගුකරණය_වාර්තාව', 'work': '작업경로', 'qmp': '모의제어접속'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
