#!/usr/bin/env python3
"""기존 PUTANJA 호환 unos_p. stvaran_podaci 구현: ../Alati/stolni_Prikaz.py"""
import importlib as TAKE_VALUE
import sys as operacijski_sustav_VALUE
from pathlib import Path as PUTANJA
operacijski_sustav_VALUE.path.insert(0, str(PUTANJA(__file__).resolve().parents[1] / 'Alati'))
if __name__ == '__main__':
    import runpy as program_pokretač
    program_pokretač.run_module('stolni_Prikaz', run_name='__main__', alter_sys=True)
else:
    구현 = TAKE_VALUE.import_module('stolni_Prikaz')
    mapiranje_VALUE = {'count': 'unos_COUNT', 'special': '특수글쇠', 'error': 'GREŠKA', 'exact': 'EXACT_VALUE', 'network': 'mreža', 'closed': '닫힘', 'length': '길이', 'opened': '열림', 'ftp_port': 'prijenos_datoteka_broj_priključka', 'server': 'server_VALUE', 'resources': 'Resursi', 'data': 'podaci', 'shift': '윗글쇠', 'send': 'slati', 'run_desktop': 'izvršiti_stolni', 'protocol': '통신규약', 'forwards': '전달규칙들', 'host': 'domaćin', 'text': 'Tekst', 'korean': '한글여부', 'port': 'broj_priključka', 'signum': '신호번호', 'version': 'broj_verzije', 'parser': 'analizator', 'bridge': 'most', 'kind': 'područje_VALUE', 'tail': '끝부분', 'size': 'Veličina', 'previous_buttons': '이전단추', 'key': '누름값', 'y': '세로좌표', 'prefix': '앞부분', 'client': 'klijent', 'char': 'znakovni_podaci', 'work': '작업경로', 'Keyboard': 'tipkovnica', 'x': 'koordinata_x', 'down': '누르는중', 'net': 'most_unos', 'self': '자신', 'mode_changed': '입력방식알림', 'serial': '직렬입출력', 'args': 'argument_ARRAY', 'Hangul': '한글조합', 'chunk': 'fragment_VALUE', 'proc': 'Proces', 'Desktop': 'CONNECT_stolni', 'buttons': '단추들', 'thread': '작업가닥', 'pressed': '눌림', 'previous': '이전항목', 'toggle': 'SWITCH_MODE', 'command': 'Naredba', 'sock': '소켓', 'frame': '실행틀', 'ctrl': 'kontrola_Ključ', 'path': 'PUTANJA', 'cp': 'kodiranje_znakova', 'terminate': '종료시키기', 'security': 'Sigurnost', 'vnc_port': '원격화면접속번호', 'body': 'tijelo_teksta', 'index': 'LOOKUP_INDEX', 'exited': '종료됨', 'keysym': 'Ključ_simbol', 'output': '출력결과', 'keyboard': 'tipkovnica_unos', 'interrupted': '가로채기됨', 'listener': 'primiti_prebaciti', 'reader': 'Čitač', 'NetworkBridge': 'most_3de4fe3a', 'gui': '그림화면', 'worker': 'obrada_obaveza'}
    for 이전, redovno_artikl in mapiranje_VALUE.items():
        if hasattr(구현, redovno_artikl): globals()[이전] = getattr(구현, redovno_artikl)
