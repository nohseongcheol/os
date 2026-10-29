#!/usr/bin/env python3
"""기존 මාර්_ගය 호환 පිවිසුම_ලකුණ. තථ්_ය_දත්ත 구현: ../මෙවලම්/원격한글시험.py"""
import importlib as 가져오기
import sys as මෙහෙයුම්_පද්ධතිය_අගය
from pathlib import Path as මාර්_ගය
මෙහෙයුම්_පද්ධතිය_අගය.path.insert(0, str(මාර්_ගය(__file__).resolve().parents[1] / 'මෙවලම්'))
if __name__ == '__main__':
    import runpy as යෙදු_යෙදුම්_ලාච්චුව
    යෙදු_යෙදුම්_ලාච්චුව.run_module('원격한글시험', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('원격한글시험')
    대응 = {'wait': '기다리기', 'typing': '글자입력', 'start': 'ක්_රියාත්මක_කරන්න_2', 'profile': 'පැතිකඩ', 'focused': 'අවධානය_යොමු_කළ', 'serial': '직렬입출력', 'keys': '누름열', 'server': 'සේවාදායකය_අගය', 'log': 'ලොගය_පේළිය', 'args': 'විස්තාරකය_ආරා_ව', 'deadline': '마감시각', 'data': 'දත්ත', 'candidate': '후보', 'logs': '기록들', 'kw': '이름붙인인수', 'number': '수치', 'main': 'ක්_රියාත්මක_කරන්න_2', 'ready': '준비완료', 'found': '찾은결과', 'guest': 'අමුත්තා', 'ROOT': '기준', 'marker': '확인표시', 'text': 'පෙළ', 'out': '결과자료', 'env': '환경', 'f': 'ගොනුව_පිවිසුම', 'port': '접속번호', 'offset': 'ඕෆ්සෙට්_අගය', 'version': '판번호', 'p': '자료위치', 'selector': 'වරකය', 'xvfb': 'අතථ්_ය_සංදර්ශකය', 'display': 'සංදර්ශකය', 'n': '개수', 'key': '누름값', 'processes': '실행과정들', 'rootfs': '뿌리파일계층', 'xdo': '가상입력도구', 'name': 'නම', 'window': 'කවුළුව', 'report': 'වලංගුකරණය_වාර්තාව', 'work': '작업경로'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
