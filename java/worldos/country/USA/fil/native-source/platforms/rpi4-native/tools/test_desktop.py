#!/usr/bin/env python3
"""기존 path 호환 pagpasok_point. totoo_data 구현: ../Mga_Tool/바탕화면시험.py"""
import importlib as TAKE_VALUE
import sys as operating_system_VALUE
from pathlib import Path as path
operating_system_VALUE.path.insert(0, str(path(__file__).resolve().parents[1] / 'Mga_Tool'))
if __name__ == '__main__':
    import runpy as app_launcher
    app_launcher.run_module('바탕화면시험', run_name='__main__', alter_sys=True)
else:
    구현 = TAKE_VALUE.import_module('바탕화면시험')
    대응 = {'x': 'x_coordinate', 'typing': '글자입력', 'message': '알림문', 'start': 'run', 'down': '누르는중', 'exact': 'EXACT_VALUE', 'i': '순번', 'press': '글쇠누르기', 'rectangles': '사각형들', 'sym': 'simbolo', 'j': '안쪽순번', 'deadline': '마감시각', 'proc': 'Proseso', 'data': 'data', 'main': 'run', 'w': '너비값', 'init': '초기값', 'block': 'data_i_block', 'ROOT': 'Project_root', 'text': 'SMS', 'marker': '확인표시', 'report': 'pagpapatibay_ulat', 'until': '까지', 'clipboard': 'clipboard_VALUE', 'dst': 'patutunguhan_email', 'seen': '본항목들', 'poll': '준비살피미', 'transcript': '대화기록', 'port': 'numero_ng_port', 'offset': 'OFFSET_VALUE', 'h': '높이값', 'src': '원본주소', 'event': 'kaganapan', 'encoding': 'set_ng_karakter', 'size': 'sukat_82232621', 'key': '누름값', 'pixels': '화소들', 'y': 'Y_button_coordinate', 'output': '출력결과', 'symbol': 'simbolo_VALUE', 'client': 'client', 'char': 'karakter_data', 'rgb': '빛삼원색'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
