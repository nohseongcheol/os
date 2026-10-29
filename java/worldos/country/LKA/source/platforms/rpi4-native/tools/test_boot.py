#!/usr/bin/env python3
"""기존 මාර්_ගය 호환 පිවිසුම_ලකුණ. තථ්_ය_දත්ත 구현: ../මෙවලම්/부팅시험.py"""
import importlib as 가져오기
import sys as මෙහෙයුම්_පද්ධතිය_අගය
from pathlib import Path as මාර්_ගය
මෙහෙයුම්_පද්ධතිය_අගය.path.insert(0, str(මාර්_ගය(__file__).resolve().parents[1] / 'මෙවලම්'))
if __name__ == '__main__':
    import runpy as යෙදු_යෙදුම්_ලාච්චුව
    යෙදු_යෙදුම්_ලාච්චුව.run_module('부팅시험', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('부팅시험')
    대응 = {'timeout': '시간제한', 'response': '응답자료', 'msg': 'ජාලය_පණිවිඩය', 'exact': '정확한값', 'markers': '확인표시들', 'i': '순번', 'match': '일치', 'execute': 'ක්_රියාත්මක_කරන්න', 'cancel': 'එපා_මෙහෙයුම', 'cmd_byte': 'විධානය_බයිටය', 'reply': 'පිළිතුරු_දෙන්න', 'points': '지점들', 'server': 'සේවාදායකය_අගය', 'data': 'දත්ත', 'prompt': 'ප්_රේරකය', 'enter': 'ඇතුල්_කිරීම', 'imported': '들여온파일', 'send': 'ඊමේල්', 'main': 'ක්_රියාත්මක_කරන්න_2', 'ROOT': '기준', 'text': 'පෙළ', 'first_gui': '첫화면', 'pixel': 'පික්සලය', 'java_class': '자바클래스', 'upload': 'උඩුගත_කරන්න_ගොනු', 'pixels_file': 'පික්සලය_ගොනුව', 'pixels_data': 'පික්සලය_දත්ත', 'edit': 'සකසන්න_අගය', 'receive_until': '표시까지받기', 'selector': 'වරකය', 'size': 'ප්_රමාණය', 'qmp_path': '모의제어경로', 'key': '누름값', 'second_gui': '둘째화면', 'y': '세로좌표', 'result': '결과', 'samples': '예제들', 'client': 'සේවාලාභීයා', 'line': 'පේළිය', 'report': 'වලංගුකරණය_වාර්තාව', 'work': '작업경로', 'x': 'x_ඛණ්ඩාංකය', 'python_checks': '파이썬검사', 'download': 'බාගන්න', 'greeting': '인사', 'dims': '치수', 'chunk': '조각', 'deadline': '마감시각', 'proc': 'සැකසුම', 'content': 'අන්තර්ගතය_අගය', 'block': 'දත්ත_අවහිර_කරන්න', 'marker': '확인표시', 'command': 'විධානය', 'expected': '예상결과', 'shell': 'කවචය', 'drawing': 'චිත්_රය_පෙත', 'f': 'ගොනුව_පිවිසුම', 'transcript': '대화기록', 'offset': 'ඕෆ්සෙට්_අගය', 'path': 'මාර්_ගය', 'screenshot': 'තිර_ඇමිණුම', 'arguments': '전달인수', 'pixels': '화소들', 'viewer': '화면접속자', 'output': '출력결과', 'stream': 'දහර_අගය', 'cmd': '명령인수', 'name': 'නම', 'qmp': '모의제어접속'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
