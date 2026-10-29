#!/usr/bin/env python3
"""기존 path 호환 pagpasok_point. totoo_data 구현: ../Mga_Tool/예제시험.py"""
import importlib as TAKE_VALUE
import sys as operating_system_VALUE
from pathlib import Path as path
operating_system_VALUE.path.insert(0, str(path(__file__).resolve().parents[1] / 'Mga_Tool'))
if __name__ == '__main__':
    import runpy as app_launcher
    app_launcher.run_module('예제시험', run_name='__main__', alter_sys=True)
else:
    구현 = TAKE_VALUE.import_module('예제시험')
    대응 = {'count': 'pagpasok_COUNT', 'exact': 'EXACT_VALUE', 'expected_file': '예상파일', 'ftp_port': 'file_lipat_numero_ng_port', 'data': 'data', 'graphics_command': 'graphics_utos', 'main': 'run', 'row': 'ROW_posisyon', 'init': '초기값', 'target': 'layunin', 'ROOT': 'Project_root', 'text': 'SMS', 'binary': 'binary', 'out': 'sukat_data', 'entry': 'pagpasok_point', 'got': 'RECEIVED_COUNT', 'port': 'numero_ng_port', 'graphics_start': 'Start_iginuhit', 'col': 'kolum_posisyon', 'begin': 'Start_OFFSET', 'kind': 'kategorya_VALUE', 'selector': 'tagapili', 'n': 'item_COUNT', 'key': '누름값', 'y': 'Y_button_coordinate', 'client': 'client', 'line': 'linya', 'report': 'pagpapatibay_ulat', 'language': 'Wika', 'x': 'x_coordinate', 'start': 'run', 'rgb': '빛삼원색', 'down': '누르는중', 'listing': 'i_email_list', 'payload': 'payload_data', 'proc': 'Proseso', 'w': '너비값', 'temporary': '임시자원', 'echo': '되돌림서버항목', 'label': 'pangalan_talahanayan', 'content': 'Nilalaman_VALUE', 'argument': '전달값', 'EchoServers': '되돌림서버', 'marker': '확인표시', 'expected': '예상결과', 'test_language': 'test_언어', 'filename': 'file_pagpasok_pangalan', 'shell': 'shell', 'color': '색상', 'transcript': '대화기록', 'offset': 'OFFSET_VALUE', 'h': '높이값', 'run': 'Mag_execute_utos', 'c': 'character_code', 'path': 'path', 'encoding': 'set_ng_karakter', 'end': 'tapusin_OFFSET', 'ftp': 'file_lipat_koneksyon', 'pixels': '화소들', 'symbol': 'simbolo_VALUE', 'source': '원본자료', 'name': 'pangalan', 'receive': '수신하기', 'manifest': '꾸러미명세'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
