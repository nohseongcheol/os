#!/usr/bin/env python3
"""기존 path 호환 pagpasok_point. totoo_data 구현: ../Mga_Tool/desktop_View.py"""
import importlib as TAKE_VALUE
import sys as operating_system_VALUE
from pathlib import Path as path
operating_system_VALUE.path.insert(0, str(path(__file__).resolve().parents[1] / 'Mga_Tool'))
if __name__ == '__main__':
    import runpy as app_launcher
    app_launcher.run_module('desktop_View', run_name='__main__', alter_sys=True)
else:
    구현 = TAKE_VALUE.import_module('desktop_View')
    대응 = {'count': 'pagpasok_COUNT', 'special': '특수글쇠', 'error': 'error', 'exact': 'EXACT_VALUE', 'network': 'Network', 'closed': '닫힘', 'length': 'haba_VALUE', 'opened': '열림', 'ftp_port': 'file_lipat_numero_ng_port', 'server': 'server_VALUE', 'resources': 'Resources', 'data': 'data', 'shift': 'SHIFT_key', 'send': 'i_email', 'run_desktop': 'run_desktop', 'protocol': '통신규약', 'forwards': '전달규칙들', 'host': 'host', 'text': 'SMS', 'korean': '한글여부', 'port': 'numero_ng_port', 'signum': '신호번호', 'version': '판번호', 'parser': 'parser', 'bridge': 'bridge', 'kind': 'kategorya_VALUE', 'tail': '끝부분', 'size': 'sukat_82232621', 'previous_buttons': '이전단추', 'key': '누름값', 'y': 'Y_button_coordinate', 'prefix': '앞부분', 'client': 'client', 'char': 'karakter_data', 'work': '작업경로', 'Keyboard': 'keyboard', 'x': 'x_coordinate', 'down': '누르는중', 'net': 'Network_bridge_pagpasok', 'self': '자신', 'mode_changed': '입력방식알림', 'serial': '직렬입출력', 'args': 'argumento_ARRAY', 'Hangul': '한글조합', 'chunk': '조각', 'proc': 'Proseso', 'Desktop': 'CONNECT_desktop', 'buttons': '단추들', 'thread': '작업가닥', 'pressed': '눌림', 'previous': '이전항목', 'toggle': 'SWITCH_MODE', 'command': 'utos', 'sock': '소켓', 'frame': '실행틀', 'ctrl': 'CTRL', 'path': 'path', 'cp': 'karakter_pag_encode', 'terminate': '종료시키기', 'security': 'Seguridad', 'vnc_port': '원격화면접속번호', 'body': 'teksto_ng_nilalaman', 'index': 'LOOKUP_INDEX', 'exited': '종료됨', 'keysym': 'key_simbolo', 'output': '출력결과', 'keyboard': 'keyboard_pagpasok', 'interrupted': '가로채기됨', 'listener': '수신창구', 'reader': 'Tagabasa', 'NetworkBridge': 'Network_bridge', 'gui': '그림화면', 'worker': '처리작업'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
