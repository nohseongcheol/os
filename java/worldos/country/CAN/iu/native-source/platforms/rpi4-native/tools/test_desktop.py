#!/usr/bin/env python3
"""기존 aqqut 호환 Iliniku_puinti. taannallarik_titiqqat 구현: ../도구/바탕화면시험.py"""
import importlib as 가져오기
import sys as qarasaujakkut_aulattijjut_atuutilik
from pathlib import Path as aqqut
qarasaujakkut_aulattijjut_atuutilik.path.insert(0, str(aqqut(__file__).resolve().parents[1] / '도구'))
if __name__ == '__main__':
    import runpy as 실행기
    실행기.run_module('바탕화면시험', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('바탕화면시험')
    대응 = {'x': '가로좌표', 'typing': '글자입력', 'message': '알림문', 'start': '시작', 'down': '누르는중', 'exact': '정확한값', 'i': '순번', 'press': '글쇠누르기', 'rectangles': '사각형들', 'sym': '기호', 'j': '안쪽순번', 'deadline': '마감시각', 'proc': 'Pivallianiq', 'data': 'titiqqat', 'main': '시작', 'w': '너비값', 'init': '초기값', 'block': 'titiqqat_sapummili', 'ROOT': '기준', 'text': 'titiqqaq', 'marker': '확인표시', 'report': 'naammannirainiq_unikkaaq', 'until': '까지', 'clipboard': 'ilijagakkuvik_atuutilik', 'dst': 'namunngarvik_turaarut', 'seen': '본항목들', 'poll': '준비살피미', 'transcript': '대화기록', 'port': '접속번호', 'offset': '변위', 'h': '높이값', 'src': '원본주소', 'event': 'piniku', 'encoding': 'immikkuungauqtut', 'size': 'anininga', 'key': '누름값', 'pixels': '화소들', 'y': '세로좌표', 'output': '출력결과', 'symbol': '심볼', 'client': 'pijittiqtaq', 'char': 'immikkuuqtuq_titiqqat', 'rgb': '빛삼원색'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
