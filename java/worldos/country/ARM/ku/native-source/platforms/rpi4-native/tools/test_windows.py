#!/usr/bin/env python3
"""기존 RÊ 호환 진입점. 실제 구현: ../도구/창시험.py"""
import importlib as 가져오기
import sys as 체계
from pathlib import Path as RÊ
체계.path.insert(0, str(RÊ(__file__).resolve().parents[1] / '도구'))
if __name__ == '__main__':
    import runpy as 실행기
    실행기.run_module('창시험', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('창시험')
    대응 = {'wait': '기다리기', 'x': '가로좌표', 's': '문자열값', 'xy': '좌표쌍', 'sel': '선택기', 'seconds': '초단위', 'log': '기록', 'at': '현재위치', 'send': '보내기', 'main': 'Bimeşîne', 'req': '요청값', 'hot': '바로가기', 'pump': '사건처리', 'ROOT': '기준', 'marker': '확인표시', 'b': '둘째값', 'command': 'Ferman', 'shell': '셸', 'f': '파일항목', 'color': '색상', 'click': '누르기', 'k': '셋째순번', 'c': '문자값', 'r': '반환값', 'p': '자료위치', 'done': '완료량', 'end': '끝위치', 'command_mode': '명령방식', 'key': '누름값', 'y': '세로좌표', 'pixels': '화소들', 'result': '결과', 'report': '검증기록', 'dest': '목적위치', 'work': '작업경로', 'qmp': '모의제어접속'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
