#!/usr/bin/env python3
"""기존 Pad 호환 inskrywing_p. werklik_data 구현: ../Nutsmiddels/바탕화면시험.py"""
import importlib as TAKE_VALUE
import sys as bedryfstelsel_VALUE
from pathlib import Path as Pad
bedryfstelsel_VALUE.path.insert(0, str(Pad(__file__).resolve().parents[1] / 'Nutsmiddels'))
if __name__ == '__main__':
    import runpy as program_oopmaker
    program_oopmaker.run_module('바탕화면시험', run_name='__main__', alter_sys=True)
else:
    구현 = TAKE_VALUE.import_module('바탕화면시험')
    대응 = {'x': 'x_koördinaat', 'typing': '글자입력', 'message': '알림문', 'start': 'Loop', 'down': '누르는중', 'exact': 'EXACT_VALUE', 'i': '순번', 'press': 'druk_Sleutel', 'rectangles': '사각형들', 'sym': 'simbool', 'j': '안쪽순번', 'deadline': '마감시각', 'proc': 'Proses', 'data': 'data', 'main': 'Loop', 'w': '너비값', 'init': '초기값', 'block': 'data_blokkeer', 'ROOT': 'Project_wortel', 'text': 'Teks', 'marker': '확인표시', 'report': 'validering_verslag', 'until': '까지', 'clipboard': 'knipbord_VALUE', 'dst': 'bestemming_adres', 'seen': '본항목들', 'poll': '준비살피미', 'transcript': '대화기록', 'port': '접속번호', 'offset': 'OFFSET_VALUE', 'h': '높이값', 'src': '원본주소', 'event': 'gebeurtenis', 'encoding': 'karakterstel', 'size': 'Grootte', 'key': '누름값', 'pixels': '화소들', 'y': 'Y_koördinaat', 'output': '출력결과', 'symbol': 'simbool_VALUE', 'client': 'kliënt', 'char': 'karakter_data', 'rgb': '빛삼원색'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
