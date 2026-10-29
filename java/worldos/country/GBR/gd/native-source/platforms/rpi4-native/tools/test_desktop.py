#!/usr/bin/env python3
"""기존 Slighe 호환 cur_a_steach_puing. dearbh_dàta 구현: ../innealan/바탕화면시험.py"""
import importlib as TAKE_VALUE
import sys as siostam_obrachaidh_VALUE
from pathlib import Path as Slighe
siostam_obrachaidh_VALUE.path.insert(0, str(Slighe(__file__).resolve().parents[1] / 'innealan'))
if __name__ == '__main__':
    import runpy as ap_drathair_nan_aplacaid
    ap_drathair_nan_aplacaid.run_module('바탕화면시험', run_name='__main__', alter_sys=True)
else:
    구현 = TAKE_VALUE.import_module('바탕화면시험')
    대응 = {'x': 'co_chomharra_x', 'typing': '글자입력', 'message': '알림문', 'start': 'ruith', 'down': '누르는중', 'exact': 'EXACT_VALUE', 'i': '순번', 'press': '글쇠누르기', 'rectangles': '사각형들', 'sym': 'samhla', 'j': '안쪽순번', 'deadline': '마감시각', 'proc': 'Pròiseas', 'data': 'dàta', 'main': 'ruith', 'w': '너비값', 'init': '초기값', 'block': 'dàta_bac', 'ROOT': 'tilg_freumh', 'text': 'SMS', 'marker': '확인표시', 'report': 'dearbhadh_aithisg', 'until': '까지', 'clipboard': 'bòrd_stòraidh_VALUE', 'dst': 'ceann_uidhe_ADDRESS', 'seen': '본항목들', 'poll': '준비살피미', 'transcript': '대화기록', 'port': '접속번호', 'offset': 'OFFSET_VALUE', 'h': '높이값', 'src': '원본주소', 'event': 'tachartas', 'encoding': 'seata_charactaran', 'size': 'atharraich_am_meud', 'key': '누름값', 'pixels': '화소들', 'y': '세로좌표', 'output': '출력결과', 'symbol': 'samhla_VALUE', 'client': 'cliant', 'char': 'caractar_dàta', 'rgb': '빛삼원색'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
