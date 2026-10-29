#!/usr/bin/env python3
"""기존 path 호환 pagpasok_point. totoo_data 구현: ../Mga_Tool/원격한글시험.py"""
import importlib as TAKE_VALUE
import sys as operating_system_VALUE
from pathlib import Path as path
operating_system_VALUE.path.insert(0, str(path(__file__).resolve().parents[1] / 'Mga_Tool'))
if __name__ == '__main__':
    import runpy as app_launcher
    app_launcher.run_module('원격한글시험', run_name='__main__', alter_sys=True)
else:
    구현 = TAKE_VALUE.import_module('원격한글시험')
    대응 = {'wait': '기다리기', 'typing': '글자입력', 'start': 'run', 'profile': 'Profile', 'focused': 'Focused', 'serial': '직렬입출력', 'keys': '누름열', 'server': 'server_VALUE', 'log': 'LOG_hanay', 'args': 'argumento_ARRAY', 'deadline': '마감시각', 'data': 'data', 'candidate': '후보', 'logs': '기록들', 'kw': '이름붙인인수', 'number': '수치', 'main': 'run', 'ready': '준비완료', 'found': 'SEARCH_sukat', 'guest': 'bisita', 'ROOT': 'Project_root', 'marker': '확인표시', 'text': 'SMS', 'out': 'sukat_data', 'env': '환경', 'f': 'file_pagpasok', 'port': 'numero_ng_port', 'offset': 'OFFSET_VALUE', 'version': '판번호', 'p': 'data_posisyon', 'selector': 'tagapili', 'xvfb': 'virtual_display', 'display': 'display', 'n': 'item_COUNT', 'key': '누름값', 'processes': '실행과정들', 'rootfs': '뿌리파일계층', 'xdo': '가상입력도구', 'name': 'pangalan', 'window': 'window', 'report': 'pagpapatibay_ulat', 'work': '작업경로'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
