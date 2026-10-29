#!/usr/bin/env python3
"""기존 path 호환 pagpasok_point. totoo_data 구현: ../Mga_Tool/셸시험.py"""
import importlib as TAKE_VALUE
import sys as operating_system_VALUE
from pathlib import Path as path
operating_system_VALUE.path.insert(0, str(path(__file__).resolve().parents[1] / 'Mga_Tool'))
if __name__ == '__main__':
    import runpy as app_launcher
    app_launcher.run_module('셸시험', run_name='__main__', alter_sys=True)
else:
    구현 = TAKE_VALUE.import_module('셸시험')
    대응 = {'timeout': '시간제한', 'x': 'x_coordinate', 'msg': 'Network_email', 'i': '순번', 'reply': 'tumugon', 'call': '호출', 'args': 'argumento_ARRAY', 'chunk': '조각', 'data': 'data', 'proc': 'Proseso', 'long_text': '긴글', 'restored': '복원자료', 'send': 'i_email', 'file': 'file', 'main': 'run', 'found': 'SEARCH_sukat', 'ROOT': 'Project_root', 'text': 'SMS', 'marker': '확인표시', 'command': 'utos', 'expected': '예상결과', 'pixel': 'pel', 'shell': 'shell', 'poll': '준비살피미', 'transcript': '대화기록', 'end': 'tapusin_OFFSET', 'image': 'IMAGE', 'key': '누름값', 'y': 'Y_button_coordinate', 'output': '출력결과', 'result': 'sukat', 'client': 'client', 'line': 'linya', 'stream': 'Stream_VALUE', 'name': 'pangalan', 'value': 'VALUE', 'receive': '수신하기', 'report': 'pagpapatibay_ulat', 'work': '작업경로', 'qmp': '모의제어접속'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
