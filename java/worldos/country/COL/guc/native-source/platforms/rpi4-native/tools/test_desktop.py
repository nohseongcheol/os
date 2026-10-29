#!/usr/bin/env python3
"""기존 wopu_a_ttaaleemüin 호환 ekeroliaa_o_uchikanain. 실제 구현: ../도구/바탕화면시험.py"""
import importlib as 가져오기
import sys as a_yatawajiraaya_a_laülaasü_ajutuu
from pathlib import Path as wopu_a_ttaaleemüin
a_yatawajiraaya_a_laülaasü_ajutuu.path.insert(0, str(wopu_a_ttaaleemüin(__file__).resolve().parents[1] / '도구'))
if __name__ == '__main__':
    import runpy as 실행기
    실행기.run_module('바탕화면시험', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('바탕화면시험')
    대응 = {'x': '가로좌표', 'typing': '글자입력', 'message': '알림문', 'start': '시작', 'down': '누르는중', 'exact': '정확한값', 'i': '순번', 'press': '글쇠누르기', 'rectangles': '사각형들', 'sym': '기호', 'j': '안쪽순번', 'deadline': '마감시각', 'proc': '실행과정', 'data': 'atijaaya', 'main': '시작', 'w': '너비값', 'init': '초기값', 'block': '자료덩이', 'ROOT': '기준', 'text': '글', 'marker': '확인표시', 'report': 'anaajiaakua_ipa_achikiimaajatü', 'until': '까지', 'clipboard': 'Karalo_utapalajana_ajutuu', 'dst': 'jalamüinjatü_ejepüsee', 'seen': '본항목들', 'poll': '준비살피미', 'transcript': '대화기록', 'port': '접속번호', 'offset': '변위', 'h': '높이값', 'src': '원본주소', 'event': 'kasachiki', 'encoding': 'jeetkotchiraaya', 'size': '크기', 'key': '누름값', 'pixels': '화소들', 'y': '세로좌표', 'output': '출력결과', 'symbol': '심볼', 'client': 'matchanta', 'char': 'jeerü_atijaaya', 'rgb': '빛삼원색'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
