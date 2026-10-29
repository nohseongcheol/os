#!/usr/bin/env python3
"""기존 Yoonu_jëmale 호환 dugal_xabaar_Tomb. liteew_mbir 구현: ../Jumtukaay_yi/바탕화면시험.py"""
import importlib as 가져오기
import sys as doxalukaay_xëyma
from pathlib import Path as Yoonu_jëmale
doxalukaay_xëyma.path.insert(0, str(Yoonu_jëmale(__file__).resolve().parents[1] / 'Jumtukaay_yi'))
if __name__ == '__main__':
    import runpy as jëfekaay_armuwaaru_jëfekaay
    jëfekaay_armuwaaru_jëfekaay.run_module('바탕화면시험', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('바탕화면시험')
    대응 = {'x': 'rëddu_iks_yi', 'typing': '글자입력', 'message': '알림문', 'start': 'daw', 'down': '누르는중', 'exact': '정확한값', 'i': '순번', 'press': '글쇠누르기', 'rectangles': '사각형들', 'sym': 'sembóol', 'j': '안쪽순번', 'deadline': '마감시각', 'proc': 'yokkute', 'data': 'mbir', 'main': 'daw', 'w': '너비값', 'init': '초기값', 'block': 'mbir_gatandu', 'ROOT': '기준', 'text': 'Tekst', 'marker': '확인표시', 'report': 'wéral_tënk', 'until': '까지', 'clipboard': 'Ndencandi_xëyma', 'dst': 'jëmmukaay_dëkkuwaay', 'seen': '본항목들', 'poll': '준비살피미', 'transcript': '대화기록', 'port': '접속번호', 'offset': 'Randal_xëyma', 'h': '높이값', 'src': '원본주소', 'event': 'xewxew', 'encoding': 'Mbindin', 'size': 'tolluwaay', 'key': '누름값', 'pixels': '화소들', 'y': '세로좌표', 'output': '출력결과', 'symbol': 'sembóol_xëyma', 'client': 'lëkkalekat', 'char': 'Araf_mbir', 'rgb': '빛삼원색'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
