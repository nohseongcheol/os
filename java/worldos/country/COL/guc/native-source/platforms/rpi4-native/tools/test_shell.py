#!/usr/bin/env python3
"""기존 wopu_a_ttaaleemüin 호환 ekeroliaa_o_uchikanain. 실제 구현: ../도구/셸시험.py"""
import importlib as 가져오기
import sys as a_yatawajiraaya_a_laülaasü_ajutuu
from pathlib import Path as wopu_a_ttaaleemüin
a_yatawajiraaya_a_laülaasü_ajutuu.path.insert(0, str(wopu_a_ttaaleemüin(__file__).resolve().parents[1] / '도구'))
if __name__ == '__main__':
    import runpy as 실행기
    실행기.run_module('셸시험', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('셸시험')
    대응 = {'timeout': '시간제한', 'x': '가로좌표', 'msg': 'kusu_pütchi', 'i': '순번', 'reply': '응답', 'call': '호출', 'args': 'ajutuu_matüriisü', 'chunk': '조각', 'data': 'atijaaya', 'proc': '실행과정', 'long_text': '긴글', 'restored': '복원자료', 'send': 'ajütaa', 'file': 'anaajaalaa', 'main': '시작', 'found': '찾은결과', 'ROOT': '기준', 'text': '글', 'marker': '확인표시', 'command': 'aluwataaya', 'expected': '예상결과', 'pixel': 'pikserü', 'shell': 'aluwataalapu_u', 'poll': '준비살피미', 'transcript': '대화기록', 'end': '끝위치', 'image': 'ayaakuaa', 'key': '누름값', 'y': '세로좌표', 'output': '출력결과', 'result': '결과', 'client': 'matchanta', 'line': 'liinia', 'stream': 'palantüsü_ajutuu', 'name': '이름', 'value': 'ajutuu', 'receive': '수신하기', 'report': 'anaajiaakua_ipa_achikiimaajatü', 'work': '작업경로', 'qmp': '모의제어접속'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
