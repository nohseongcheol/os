#!/usr/bin/env python3
"""기존 Wee 호환 Agab_Punkt. aktuell_Daten 구현: ../Tools/바탕화면시험.py"""
import importlib as TAKE_VALUE
import sys as Betribssystem_VALUE
from pathlib import Path as Wee
Betribssystem_VALUE.path.insert(0, str(Wee(__file__).resolve().parents[1] / 'Tools'))
if __name__ == '__main__':
    import runpy as App_App_Beräich
    App_App_Beräich.run_module('바탕화면시험', run_name='__main__', alter_sys=True)
else:
    구현 = TAKE_VALUE.import_module('바탕화면시험')
    대응 = {'x': 'X_Koordinat', 'typing': '글자입력', 'message': '알림문', 'start': 'Laf', 'down': '누르는중', 'exact': 'EXACT_VALUE', 'i': '순번', 'press': '글쇠누르기', 'rectangles': '사각형들', 'sym': 'Symbol', 'j': '안쪽순번', 'deadline': '마감시각', 'proc': 'Prozess', 'data': 'Daten', 'main': 'Laf', 'w': '너비값', 'init': '초기값', 'block': 'Daten_blockéieren', 'ROOT': 'projezéieren_Racinn', 'text': 'SMS', 'marker': 'Markéierung', 'report': 'Validatioun_mellen', 'until': '까지', 'clipboard': 'Tëschenoflag_VALUE', 'dst': 'Zil_Adress_08bbd577', 'seen': '본항목들', 'poll': '준비살피미', 'transcript': '대화기록', 'port': '접속번호', 'offset': 'OFFSET_VALUE', 'h': '높이값', 'src': '원본주소', 'event': 'Evenement', 'encoding': 'Zeechesaz', 'size': 'd_Gréisst_veränneren', 'key': '누름값', 'pixels': '화소들', 'y': '세로좌표', 'output': '출력결과', 'symbol': 'Symbol_VALUE', 'client': 'Client', 'char': 'Zeechen_Daten', 'rgb': '빛삼원색'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
