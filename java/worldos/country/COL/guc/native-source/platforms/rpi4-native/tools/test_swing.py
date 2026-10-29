#!/usr/bin/env python3
"""기존 wopu_a_ttaaleemüin 호환 ekeroliaa_o_uchikanain. 실제 구현: ../도구/화면요소시험.py"""
import importlib as 가져오기
import sys as a_yatawajiraaya_a_laülaasü_ajutuu
from pathlib import Path as wopu_a_ttaaleemüin
a_yatawajiraaya_a_laülaasü_ajutuu.path.insert(0, str(wopu_a_ttaaleemüin(__file__).resolve().parents[1] / '도구'))
if __name__ == '__main__':
    import runpy as 실행기
    실행기.run_module('화면요소시험', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('화면요소시험')
    대응 = {'wait': '기다리기', 'x': '가로좌표', 's': 'kaleena_atijaaya', 'i': '순번', 'sel': '선택기', 'seconds': '초단위', 'log': 'aa_innachikimaajatü_aparatsee', 'data': 'atijaaya', 'at': '현재위치', 'send': 'ajütaa', 'main': '시작', 'req': '요청값', 'hot': 'a_ttaaya_uwatuale_e_ajutuu', 'pump': 'aapaaya_kasachiki', 'ROOT': '기준', 'marker': '확인표시', 'b': '둘째값', 'command': 'aluwataaya', 'shell': 'aluwataalapu_u', 'f': 'anaajaalaa_ekeroliaa', 'click': 'aküliküjaa_ajüttülee', 'k': '셋째순번', 'c': '문자값', 'r': '반환값', 'p': '자료위치', 'command_mode': 'aluwataaya_akua_ipaa', 'end': '끝위치', 'classes': 'akotchijuushi_wopu_a_ttaaleemüin', 'key': '누름값', 'y': '세로좌표', 'result': '결과', 'report': 'anaajiaakua_ipa_achikiimaajatü', 'dest': '목적위치', 'work': '작업경로', 'qmp': '모의제어접속'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
