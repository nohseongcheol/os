#!/usr/bin/env python3
"""기존 SLÓÐ 호환 færsla_P. raun_gögn 구현: ../Verkfæri/바탕화면시험.py"""
import importlib as TAKE_VALUE
import sys as stýrikerfi_VALUE
from pathlib import Path as SLÓÐ
stýrikerfi_VALUE.path.insert(0, str(SLÓÐ(__file__).resolve().parents[1] / 'Verkfæri'))
if __name__ == '__main__':
    import runpy as forrit_ræsir
    forrit_ræsir.run_module('바탕화면시험', run_name='__main__', alter_sys=True)
else:
    구현 = TAKE_VALUE.import_module('바탕화면시험')
    vörpun_VALUE = {'x': 'x_hnit', 'typing': '글자입력', 'message': '알림문', 'start': 'Keyra_2', 'down': '누르는중', 'exact': 'EXACT_VALUE', 'i': '순번', 'press': 'ýta_Lykill', 'rectangles': '사각형들', 'sym': 'tákn', 'j': '안쪽순번', 'deadline': '마감시각', 'proc': 'Ferli', 'data': 'gögn', 'main': 'Keyra_2', 'w': '너비값', 'init': '초기값', 'block': 'gögn_útiloka', 'ROOT': 'verk_rót', 'text': 'Texti', 'marker': '확인표시', 'report': 'prófun_skrá', 'until': '까지', 'clipboard': 'klippiborð_VALUE', 'dst': 'endastaður_slóð_08bbd577', 'seen': '본항목들', 'poll': '준비살피미', 'transcript': '대화기록', 'port': 'tengisnúmer', 'offset': 'OFFSET_VALUE', 'h': '높이값', 'src': '원본주소', 'event': 'atvik', 'encoding': 'stafamengi', 'size': 'Stærð', 'key': '누름값', 'pixels': '화소들', 'y': 'Y_hnit', 'output': 'úttak_54cd5e1d', 'symbol': 'tákn_VALUE', 'client': 'biðlari', 'char': 'stafur_gögn', 'rgb': '빛삼원색'}
    for 이전, 현재 in vörpun_VALUE.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
