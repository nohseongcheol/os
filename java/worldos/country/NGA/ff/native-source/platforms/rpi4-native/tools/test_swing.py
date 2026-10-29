#!/usr/bin/env python3
"""기존 laawol 호환 naatnugol_toɓɓere. laatii_keɓe 구현: ../도구/화면요소시험.py"""
import importlib as 가져오기
import sys as yuɓɓo_kurdinɗo_njaru
from pathlib import Path as laawol
yuɓɓo_kurdinɗo_njaru.path.insert(0, str(laawol(__file__).resolve().parents[1] / '도구'))
if __name__ == '__main__':
    import runpy as 실행기
    실행기.run_module('화면요소시험', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('화면요소시험')
    대응 = {'wait': '기다리기', 'x': '가로좌표', 's': 'ɓoggol_keɓe', 'i': '순번', 'sel': '선택기', 'seconds': '초단위', 'log': 'suurnal_winndande', 'data': 'keɓe', 'at': '현재위치', 'send': 'neldude', 'main': 'huutoraade', 'req': '요청값', 'hot': 'sodorde_njaru', 'pump': 'jaggoode_saɗteende', 'ROOT': '기준', 'marker': '확인표시', 'b': '둘째값', 'command': 'ginol', 'shell': 'laalagal', 'f': 'fiilde_naatnugol', 'click': 'dobaade_feɗoode', 'k': '셋째순번', 'c': '문자값', 'r': '반환값', 'p': '자료위치', 'command_mode': 'ginol_modd', 'end': '끝위치', 'classes': 'fedde_laawol', 'key': '누름값', 'y': '세로좌표', 'result': '결과', 'report': 'teeŋtingol_ciimtol', 'dest': '목적위치', 'work': '작업경로', 'qmp': '모의제어접속'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
