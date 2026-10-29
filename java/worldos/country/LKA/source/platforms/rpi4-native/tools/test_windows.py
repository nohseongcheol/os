#!/usr/bin/env python3
"""기존 මාර්_ගය 호환 පිවිසුම_ලකුණ. තථ්_ය_දත්ත 구현: ../මෙවලම්/창시험.py"""
import importlib as 가져오기
import sys as මෙහෙයුම්_පද්ධතිය_අගය
from pathlib import Path as මාර්_ගය
මෙහෙයුම්_පද්ධතිය_අගය.path.insert(0, str(මාර්_ගය(__file__).resolve().parents[1] / 'මෙවලම්'))
if __name__ == '__main__':
    import runpy as යෙදු_යෙදුම්_ලාච්චුව
    යෙදු_යෙදුම්_ලාච්චුව.run_module('창시험', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('창시험')
    대응 = {'wait': '기다리기', 'x': 'x_ඛණ්ඩාංකය', 's': 'අනුලකුණු_වැල_දත්ත', 'xy': 'ඛණ්ඩාංක_යුගලය', 'sel': 'වරකය_a916db4e', 'seconds': '초단위', 'log': 'ලොගය_පේළිය', 'at': '현재위치', 'send': 'ඊමේල්', 'main': 'ක්_රියාත්මක_කරන්න_2', 'req': '요청값', 'hot': 'කෙටිමඟ_අගය', 'pump': 'හසුරුව_සිද්ධිය', 'ROOT': '기준', 'marker': '확인표시', 'b': '둘째값', 'command': 'විධානය', 'shell': 'කවචය', 'f': 'ගොනුව_පිවිසුම', 'color': '색상', 'click': 'ක්ලික්_කරන්න_බොත්තම', 'k': '셋째순번', 'c': 'අනුලකුණු_කේතය', 'r': '반환값', 'p': '자료위치', 'done': '완료량', 'end': 'නිමා_කරන්න_ඕෆ්සෙට්', 'command_mode': 'විධානය_ප්_රකාරය', 'key': '누름값', 'y': '세로좌표', 'pixels': '화소들', 'result': '결과', 'report': 'වලංගුකරණය_වාර්තාව', 'dest': '목적위치', 'work': '작업경로', 'qmp': '모의제어접속'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
