#!/usr/bin/env python3
"""기존 Pad 호환 inskrywing_p. werklik_data 구현: ../Nutsmiddels/werkskerm_bekyk.py"""
import importlib as TAKE_VALUE
import sys as bedryfstelsel_VALUE
from pathlib import Path as Pad
bedryfstelsel_VALUE.path.insert(0, str(Pad(__file__).resolve().parents[1] / 'Nutsmiddels'))
if __name__ == '__main__':
    import runpy as program_oopmaker
    program_oopmaker.run_module('werkskerm_bekyk', run_name='__main__', alter_sys=True)
else:
    구현 = TAKE_VALUE.import_module('werkskerm_bekyk')
    대응 = {'count': 'inskrywing_COUNT', 'special': '특수글쇠', 'error': 'Fout', 'exact': 'EXACT_VALUE', 'network': 'Netwerk', 'closed': '닫힘', 'length': 'lengte_VALUE', 'opened': '열림', 'ftp_port': '파일전송접속번호', 'server': 'bediener_VALUE', 'resources': 'Hulpbronne', 'data': 'data', 'shift': 'SHIFT_sleutel', 'send': 'e_pos', 'run_desktop': 'ry_werkskerm', 'protocol': '통신규약', 'forwards': '전달규칙들', 'host': 'hou', 'text': 'Teks', 'korean': '한글여부', 'port': '접속번호', 'signum': '신호번호', 'version': '판번호', 'parser': 'ontleder', 'bridge': 'brug', 'kind': 'kategorie_VALUE', 'tail': '끝부분', 'size': 'Grootte', 'previous_buttons': '이전단추', 'key': '누름값', 'y': 'Y_koördinaat', 'prefix': '앞부분', 'client': 'kliënt', 'char': 'karakter_data', 'work': '작업경로', 'Keyboard': 'sleutelbord', 'x': 'x_koördinaat', 'down': '누르는중', 'net': 'Netwerk_brug_inskrywing', 'self': '자신', 'mode_changed': '입력방식알림', 'serial': '직렬입출력', 'args': 'argument_ARRAY', 'Hangul': '한글조합', 'chunk': '조각', 'proc': 'Proses', 'Desktop': 'KOPPEL_werkskerm', 'buttons': '단추들', 'thread': '작업가닥', 'pressed': '눌림', 'previous': '이전항목', 'toggle': 'SWITCH_MODE', 'command': 'Opdrag', 'sock': '소켓', 'frame': '실행틀', 'ctrl': 'CTRL', 'path': 'Pad', 'cp': 'karakter_enkodering', 'terminate': '종료시키기', 'security': 'Sekuriteit', 'vnc_port': '원격화면접속번호', 'body': 'inhoudteks', 'index': 'LOOKUP_INDEX', 'exited': '종료됨', 'keysym': 'Sleutel_simbool', 'output': '출력결과', 'keyboard': 'sleutelbord_inskrywing', 'interrupted': '가로채기됨', 'listener': '수신창구', 'reader': 'Leser', 'NetworkBridge': 'Netwerk_brug', 'gui': '그림화면', 'worker': '처리작업'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
