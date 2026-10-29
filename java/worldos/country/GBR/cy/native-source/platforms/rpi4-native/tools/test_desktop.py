#!/usr/bin/env python3
"""기존 LLWYBR 호환 cofnod_p. go_iawn_data 구현: ../Offer/바탕화면시험.py"""
import importlib as TAKE_VALUE
import sys as system_weithredu_VALUE
from pathlib import Path as LLWYBR
system_weithredu_VALUE.path.insert(0, str(LLWYBR(__file__).resolve().parents[1] / 'Offer'))
if __name__ == '__main__':
    import runpy as Rhaglen_lansiwr
    Rhaglen_lansiwr.run_module('바탕화면시험', run_name='__main__', alter_sys=True)
else:
    구현 = TAKE_VALUE.import_module('바탕화면시험')
    대응 = {'x': 'cyfesuryn_x', 'typing': '글자입력', 'message': '알림문', 'start': 'Gweithredu_2', 'down': '누르는중', 'exact': 'EXACT_VALUE', 'i': '순번', 'press': 'pwyso_bysell', 'rectangles': '사각형들', 'sym': 'symbol', 'j': '안쪽순번', 'deadline': '마감시각', 'proc': 'Proses', 'data': 'data', 'main': 'Gweithredu_2', 'w': '너비값', 'init': '초기값', 'block': 'data_rhwystro', 'ROOT': 'prosiect_gwraidd', 'text': 'Testun', 'marker': '확인표시', 'report': 'dilysu_adrodd', 'until': '까지', 'clipboard': 'clipfwrdd_VALUE', 'dst': 'cyrchfan_ADDRESS', 'seen': '본항목들', 'poll': '준비살피미', 'transcript': '대화기록', 'port': 'rhif_porth', 'offset': 'OFFSET_VALUE', 'h': '높이값', 'src': '원본주소', 'event': 'digwyddiad', 'encoding': 'set_nodau', 'size': 'Maint', 'key': '누름값', 'pixels': '화소들', 'y': 'Y_cyfesuryn', 'output': '출력결과', 'symbol': 'symbol_VALUE', 'client': 'cleient', 'char': 'nod_data', 'rgb': '빛삼원색'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
