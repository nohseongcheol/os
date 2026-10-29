#!/usr/bin/env python3
"""기존 path 호환 pagpasok_point. totoo_data 구현: ../Mga_Tool/부팅시험.py"""
import importlib as TAKE_VALUE
import sys as operating_system_VALUE
from pathlib import Path as path
operating_system_VALUE.path.insert(0, str(path(__file__).resolve().parents[1] / 'Mga_Tool'))
if __name__ == '__main__':
    import runpy as app_launcher
    app_launcher.run_module('부팅시험', run_name='__main__', alter_sys=True)
else:
    구현 = TAKE_VALUE.import_module('부팅시험')
    대응 = {'timeout': '시간제한', 'response': '응답자료', 'msg': 'Network_email', 'exact': 'EXACT_VALUE', 'markers': '확인표시들', 'i': '순번', 'match': '일치', 'execute': 'Mag_execute_gawain', 'cancel': 'Kanselahin_operasyon', 'cmd_byte': 'utos_byte', 'reply': 'tumugon', 'points': '지점들', 'server': 'server_VALUE', 'data': 'data', 'prompt': 'prompt', 'enter': 'magpasok', 'imported': '들여온파일', 'send': 'i_email', 'main': 'run', 'ROOT': 'Project_root', 'text': 'SMS', 'first_gui': '첫화면', 'pixel': 'pel', 'java_class': '자바클래스', 'upload': 'upload_Mga_File', 'pixels_file': 'pel_file', 'pixels_data': 'pel_data', 'edit': 'edit_VALUE', 'receive_until': '표시까지받기', 'selector': 'tagapili', 'size': 'sukat_82232621', 'qmp_path': '모의제어경로', 'key': '누름값', 'second_gui': 'SECOND_GUI', 'y': 'Y_button_coordinate', 'result': 'sukat', 'samples': '예제들', 'client': 'client', 'line': 'linya', 'report': 'pagpapatibay_ulat', 'work': '작업경로', 'x': 'x_coordinate', 'python_checks': '파이썬검사', 'download': 'download', 'greeting': '인사', 'dims': '치수', 'chunk': '조각', 'deadline': '마감시각', 'proc': 'Proseso', 'content': 'Nilalaman_VALUE', 'block': 'data_i_block', 'marker': '확인표시', 'command': 'utos', 'expected': '예상결과', 'shell': 'shell', 'drawing': 'iginuhit_path', 'f': 'file_pagpasok', 'transcript': '대화기록', 'offset': 'OFFSET_VALUE', 'path': 'path', 'screenshot': 'screenshot', 'arguments': '전달인수', 'pixels': '화소들', 'viewer': '화면접속자', 'output': '출력결과', 'stream': 'Stream_VALUE', 'cmd': '명령인수', 'name': 'pangalan', 'qmp': '모의제어접속'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
