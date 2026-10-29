#!/usr/bin/env python3
"""기존 aqqut 호환 Iliniku_puinti. taannallarik_titiqqat 구현: ../도구/화면요소시험.py"""
import importlib as 가져오기
import sys as qarasaujakkut_aulattijjut_atuutilik
from pathlib import Path as aqqut
qarasaujakkut_aulattijjut_atuutilik.path.insert(0, str(aqqut(__file__).resolve().parents[1] / '도구'))
if __name__ == '__main__':
    import runpy as 실행기
    실행기.run_module('화면요소시험', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('화면요소시험')
    대응 = {'wait': '기다리기', 'x': '가로좌표', 's': 'qimiaq_titiqqat', 'i': '순번', 'sel': '선택기', 'seconds': '초단위', 'log': 'papattivik_sanimukutaak', 'data': 'titiqqat', 'at': '현재위치', 'send': 'nassiutili', 'main': '시작', 'req': '요청값', 'hot': 'nangarut_atuutilik', 'pump': 'nuuttarut_piniku', 'ROOT': '기준', 'marker': '확인표시', 'b': '둘째값', 'command': 'piqujijjut', 'shell': 'piqujijjutiliriji', 'f': 'ini_Iliniku', 'click': 'naqilli_tikkuagaq', 'k': '셋째순번', 'c': 'immikkuuqtumut_nalunaikkut', 'r': '반환값', 'p': '자료위치', 'command_mode': 'piqujijjut_mode', 'end': '끝위치', 'classes': 'naliannuungavik_aqqut', 'key': '누름값', 'y': '세로좌표', 'result': '결과', 'report': 'naammannirainiq_unikkaaq', 'dest': '목적위치', 'work': '작업경로', 'qmp': '모의제어접속'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
