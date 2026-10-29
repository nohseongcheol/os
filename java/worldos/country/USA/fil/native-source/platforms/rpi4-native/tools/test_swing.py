#!/usr/bin/env python3
"""기존 path 호환 pagpasok_point. totoo_data 구현: ../Mga_Tool/화면요소시험.py"""
import importlib as TAKE_VALUE
import sys as operating_system_VALUE
from pathlib import Path as path
operating_system_VALUE.path.insert(0, str(path(__file__).resolve().parents[1] / 'Mga_Tool'))
if __name__ == '__main__':
    import runpy as app_launcher
    app_launcher.run_module('화면요소시험', run_name='__main__', alter_sys=True)
else:
    구현 = TAKE_VALUE.import_module('화면요소시험')
    대응 = {'wait': '기다리기', 'x': 'x_coordinate', 's': 'string_data', 'i': '순번', 'sel': 'tagapili_a916db4e', 'seconds': '초단위', 'log': 'LOG_hanay', 'data': 'data', 'at': '현재위치', 'send': 'i_email', 'main': 'run', 'req': '요청값', 'hot': 'shortcut_VALUE', 'pump': 'hawakán_kaganapan', 'ROOT': 'Project_root', 'marker': '확인표시', 'b': 'SECOND_VALUE', 'command': 'utos', 'shell': 'shell', 'f': 'file_pagpasok', 'click': 'magklik_button', 'k': '셋째순번', 'c': 'character_code', 'r': '반환값', 'p': 'data_posisyon', 'command_mode': 'utos_MODE', 'end': 'tapusin_OFFSET', 'classes': 'kategorya_path', 'key': '누름값', 'y': 'Y_button_coordinate', 'result': 'sukat', 'report': 'pagpapatibay_ulat', 'dest': 'patutunguhan_VALUE_posisyon', 'work': '작업경로', 'qmp': '모의제어접속'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
