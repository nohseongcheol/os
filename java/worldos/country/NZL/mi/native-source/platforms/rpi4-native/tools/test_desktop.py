#!/usr/bin/env python3
"""기존 ara 호환 tāurunga_ira. tūturu_raraunga 구현: ../Ngā_Utauta/바탕화면시험.py"""
import importlib as TAKE_uara
import sys as pūnaha_mahi_uara
from pathlib import Path as ara
pūnaha_mahi_uara.path.insert(0, str(ara(__file__).resolve().parents[1] / 'Ngā_Utauta'))
if __name__ == '__main__':
    import runpy as kaupapa_pūwhiri_taupānga
    kaupapa_pūwhiri_taupānga.run_module('바탕화면시험', run_name='__main__', alter_sys=True)
else:
    구현 = TAKE_uara.import_module('바탕화면시험')
    대응 = {'x': 'taunga_x', 'typing': '글자입력', 'message': '알림문', 'start': 'whakahaere', 'down': '누르는중', 'exact': 'EXACT_uara', 'i': '순번', 'press': '글쇠누르기', 'rectangles': '사각형들', 'sym': 'tohu', 'j': '안쪽순번', 'deadline': '마감시각', 'proc': 'Hātepe', 'data': 'raraunga', 'main': 'whakahaere', 'w': '너비값', 'init': '초기값', 'block': 'raraunga_aukati', 'ROOT': 'whakaatu_pūtake', 'text': 'Ngā_kupu', 'marker': '확인표시', 'report': 'whakamana_pūrongo', 'until': '까지', 'clipboard': 'papatopenga_uara', 'dst': 'ūnga_ADDRESS_08bbd577', 'seen': '본항목들', 'poll': '준비살피미', 'transcript': '대화기록', 'port': '접속번호', 'offset': 'OFFSET_uara', 'h': '높이값', 'src': '원본주소', 'event': 'hui', 'encoding': 'rōpū_pūāhua', 'size': 'rahi', 'key': '누름값', 'pixels': '화소들', 'y': '세로좌표', 'output': '출력결과', 'symbol': 'tohu_uara', 'client': 'kiritaki', 'char': 'pūāhua_raraunga', 'rgb': '빛삼원색'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
