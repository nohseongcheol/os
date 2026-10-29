#!/usr/bin/env python3
"""기존 Putanja 호환 unos_p. stvaran_podaci 구현: ../Alati/desktop_Prikaz.py"""
import importlib as TAKE_VALUE
import sys as operativni_sistem_VALUE
from pathlib import Path as Putanja
operativni_sistem_VALUE.path.insert(0, str(Putanja(__file__).resolve().parents[1] / 'Alati'))
if __name__ == '__main__':
    import runpy as program_pokretač
    program_pokretač.run_module('desktop_Prikaz', run_name='__main__', alter_sys=True)
else:
    구현 = TAKE_VALUE.import_module('desktop_Prikaz')
    대응 = {'count': 'unos_COUNT', 'special': '특수글쇠', 'error': 'GRESKA', 'exact': 'EXACT_VALUE', 'network': 'Mreža', 'closed': '닫힘', 'length': 'dužina_VALUE', 'opened': '열림', 'ftp_port': 'fajl_prijenos_broj_priključka', 'server': 'server_VALUE', 'resources': 'Resursi', 'data': 'podaci', 'shift': 'tipka_SHIFT', 'send': 'poslati', 'run_desktop': 'niz_desktop', 'protocol': '통신규약', 'forwards': '전달규칙들', 'host': 'organizator', 'text': 'Tekst', 'korean': '한글여부', 'port': 'broj_priključka', 'signum': '신호번호', 'version': 'broj_verzije', 'parser': '인수해석기', 'bridge': 'most', 'kind': 'oblast_VALUE', 'tail': '끝부분', 'size': 'Veličina', 'previous_buttons': '이전단추', 'key': '누름값', 'y': 'Y_koordinata', 'prefix': '앞부분', 'client': 'klijent', 'char': 'znak_podaci', 'work': '작업경로', 'Keyboard': 'tastatura', 'x': 'koordinata_x', 'down': '누르는중', 'net': 'Mreža_most_unos', 'self': '자신', 'mode_changed': '입력방식알림', 'serial': '직렬입출력', 'args': 'argument_niz', 'Hangul': '한글조합', 'chunk': '조각', 'proc': 'proces', 'Desktop': 'povezati_desktop', 'buttons': '단추들', 'thread': '작업가닥', 'pressed': '눌림', 'previous': '이전항목', 'toggle': 'SWITCH_mod', 'command': 'Naredba', 'sock': '소켓', 'frame': '실행틀', 'ctrl': 'CTRL', 'path': 'Putanja', 'cp': 'znak_kodiranje', 'terminate': '종료시키기', 'security': 'Sigurnost', 'vnc_port': '원격화면접속번호', 'body': 'tijelo_teksta', 'index': 'LOOKUP_INDEX', 'exited': '종료됨', 'keysym': 'ključ_simbol', 'output': '출력결과', 'keyboard': 'tastatura_unos', 'interrupted': '가로채기됨', 'listener': '수신창구', 'reader': 'Čitač', 'NetworkBridge': 'Mreža_most', 'gui': '그림화면', 'worker': '처리작업'}
    for 이전, trenutno_stavka in 대응.items():
        if hasattr(구현, trenutno_stavka): globals()[이전] = getattr(구현, trenutno_stavka)
