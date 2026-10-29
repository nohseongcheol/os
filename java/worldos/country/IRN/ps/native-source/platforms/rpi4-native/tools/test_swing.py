#!/usr/bin/env python3
"""기존 يونلور 호환 ننوت_ټکى. 실제 구현: ../도구/화면요소시험.py"""
import importlib as 가져오기
import sys as چليز_غونډال_ارزښت
from pathlib import Path as يونلور
چليز_غونډال_ارزښت.path.insert(0, str(يونلور(__file__).resolve().parents[1] / '도구'))
if __name__ == '__main__':
    import runpy as 실행기
    실행기.run_module('화면요소시험', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('화면요소시험')
    대응 = {'wait': '기다리기', 'x': '가로좌표', 's': 'مزى_اومتوک', 'i': '순번', 'sel': '선택기', 'seconds': '초단위', 'log': 'خبرال_کیل', 'data': 'اومتوک', 'at': '현재위치', 'send': 'استول', 'main': 'ځغلول', 'req': '요청값', 'hot': 'لنډلار_ارزښت', 'pump': 'لاستى_پېښه', 'ROOT': '기준', 'marker': '확인표시', 'b': '둘째값', 'command': 'بولۍ', 'shell': 'سیپۍ', 'f': 'دوتنه_ننوت', 'click': 'ټک_تڼۍ', 'k': '셋째순번', 'c': '문자값', 'r': '반환값', 'p': '자료위치', 'command_mode': 'بولۍ_اکر', 'end': '끝위치', 'classes': 'پاړکى_يونلور', 'key': '누름값', 'y': '세로좌표', 'result': '결과', 'report': 'باورکړن_راپور', 'dest': '목적위치', 'work': '작업경로', 'qmp': '모의제어접속'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
