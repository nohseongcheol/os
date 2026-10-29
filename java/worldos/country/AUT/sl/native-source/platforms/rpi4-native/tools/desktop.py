#!/usr/bin/env python3
"""기존 POT 호환 vnos_p. dejanski_podatki 구현: ../Orodja/namizje_Pogled.py"""
import importlib as TAKE_VALUE
import sys as operacijski_sistem_VALUE
from pathlib import Path as POT
operacijski_sistem_VALUE.path.insert(0, str(POT(__file__).resolve().parents[1] / 'Orodja'))
if __name__ == '__main__':
    import runpy as aplikacija_zaganjalnik
    aplikacija_zaganjalnik.run_module('namizje_Pogled', run_name='__main__', alter_sys=True)
else:
    구현 = TAKE_VALUE.import_module('namizje_Pogled')
    preslikava_VALUE = {'count': 'vnos_COUNT', 'special': '특수글쇠', 'error': 'NAPAKA', 'exact': 'EXACT_VALUE', 'network': 'mreža', 'closed': '닫힘', 'length': '길이', 'opened': '열림', 'ftp_port': 'prenos_datotek_številka_vrat', 'server': 'strežnik_VALUE', 'resources': 'Viri', 'data': 'podatki', 'shift': 'tipka_SHIFT', 'send': 'poslati', 'run_desktop': 'izvajati_namizje', 'protocol': '통신규약', 'forwards': '전달규칙들', 'host': 'gostiti', 'text': 'Besedilo', 'korean': '한글여부', 'port': 'številka_vrat', 'signum': '신호번호', 'version': 'številka_različice', 'parser': 'razčlenjevalnik', 'bridge': 'most', 'kind': 'območje_VALUE', 'tail': '끝부분', 'size': 'Velikost', 'previous_buttons': '이전단추', 'key': '누름값', 'y': '세로좌표', 'prefix': '앞부분', 'client': 'odjemalec', 'char': 'znakovni_podatki', 'work': '작업경로', 'Keyboard': 'tipkovnica', 'x': 'koordinata_x', 'down': '누르는중', 'net': 'most_vnos', 'self': '자신', 'mode_changed': '입력방식알림', 'serial': '직렬입출력', 'args': 'argument_ARRAY', 'Hangul': '한글조합', 'chunk': '조각', 'proc': 'Opravilo', 'Desktop': 'POVEŽI_namizje', 'buttons': '단추들', 'thread': '작업가닥', 'pressed': '눌림', 'previous': '이전항목', 'toggle': 'SWITCH_MODE', 'command': 'Ukaz', 'sock': 'vtičnica_VALUE', 'frame': '실행틀', 'ctrl': 'nadzor_Ključ', 'path': 'POT', 'cp': 'kodiranje_znakov', 'terminate': '종료시키기', 'security': 'Varnost', 'vnc_port': '원격화면접속번호', 'body': 'telo_besedila', 'index': 'LOOKUP_INDEX', 'exited': '종료됨', 'keysym': 'Ključ_simbol', 'output': '출력결과', 'keyboard': 'tipkovnica_vnos', 'interrupted': '가로채기됨', 'listener': 'sprejeti_sprejemati_prejeti_prejemati_vrata', 'reader': 'bralec', 'NetworkBridge': 'most_3de4fe3a', 'gui': '그림화면', 'worker': 'obdelava_opravek'}
    for 이전, sprotno_element in preslikava_VALUE.items():
        if hasattr(구현, sprotno_element): globals()[이전] = getattr(구현, sprotno_element)
