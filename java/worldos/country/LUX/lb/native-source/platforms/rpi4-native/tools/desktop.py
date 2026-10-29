#!/usr/bin/env python3
"""기존 Wee 호환 Agab_Punkt. aktuell_Daten 구현: ../Tools/Desktop_Vue.py"""
import importlib as TAKE_VALUE
import sys as Betribssystem_VALUE
from pathlib import Path as Wee
Betribssystem_VALUE.path.insert(0, str(Wee(__file__).resolve().parents[1] / 'Tools'))
if __name__ == '__main__':
    import runpy as App_App_Beräich
    App_App_Beräich.run_module('Desktop_Vue', run_name='__main__', alter_sys=True)
else:
    구현 = TAKE_VALUE.import_module('Desktop_Vue')
    대응 = {'count': 'Agab_COUNT', 'special': '특수글쇠', 'error': 'Feeler', 'exact': 'EXACT_VALUE', 'network': 'Reseau', 'closed': '닫힘', 'length': 'Längt_VALUE', 'opened': '열림', 'ftp_port': '파일전송접속번호', 'server': 'Server_VALUE', 'resources': 'Ressourcen', 'data': 'Daten', 'shift': 'SHIFT_Tast', 'send': 'mailen', 'run_desktop': 'Laf_Desktop', 'protocol': '통신규약', 'forwards': '전달규칙들', 'host': 'Host', 'text': 'SMS', 'korean': '한글여부', 'port': '접속번호', 'signum': '신호번호', 'version': '판번호', 'parser': '인수해석기', 'bridge': 'Bréck', 'kind': 'Kategorie_VALUE', 'tail': '끝부분', 'size': 'd_Gréisst_veränneren', 'previous_buttons': '이전단추', 'key': '누름값', 'y': '세로좌표', 'prefix': '앞부분', 'client': 'Client', 'char': 'Zeechen_Daten', 'work': '작업경로', 'Keyboard': 'Tastatur', 'x': 'X_Koordinat', 'down': '누르는중', 'net': 'Reseau_Bréck_Agab', 'self': '자신', 'mode_changed': '입력방식알림', 'serial': '직렬입출력', 'args': 'Argument_ARRAY', 'Hangul': '한글조합', 'chunk': '조각', 'proc': 'Prozess', 'Desktop': 'Verbannen_Desktop', 'buttons': '단추들', 'thread': '작업가닥', 'pressed': '눌림', 'previous': '이전항목', 'toggle': 'SWITCH_MODE', 'command': 'Befeel', 'sock': '소켓', 'frame': '실행틀', 'ctrl': 'CTRL', 'path': 'Wee', 'cp': 'Zeechen_Codéierung', 'terminate': '종료시키기', 'security': 'Sécherheet', 'vnc_port': '원격화면접속번호', 'body': 'Textkierper', 'index': 'LOOKUP_INDEX', 'exited': '종료됨', 'keysym': 'Tast_Symbol', 'output': '출력결과', 'keyboard': 'Tastatur_Agab', 'interrupted': '가로채기됨', 'listener': '수신창구', 'reader': 'Lieser', 'NetworkBridge': 'Reseau_Bréck', 'gui': '그림화면', 'worker': '처리작업'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
