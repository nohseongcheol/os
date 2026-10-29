#!/usr/bin/env python3
"""기존 putanja 호환 stavka_p. stvarni_podaci 구현: ../Alatke/desktop_Prikaz.py"""
import importlib as TAKE_VALUE
import sys as operativni_sistem_VALUE
from pathlib import Path as putanja
operativni_sistem_VALUE.path.insert(0, str(putanja(__file__).resolve().parents[1] / 'Alatke'))
if __name__ == '__main__':
    import runpy as program_pokretač
    program_pokretač.run_module('desktop_Prikaz', run_name='__main__', alter_sys=True)
else:
    구현 = TAKE_VALUE.import_module('desktop_Prikaz')
    mapiranje_VALUE = {'count': 'stavka_COUNT_8f7753a1', 'special': '특수글쇠', 'error': 'greška', 'exact': 'EXACT_VALUE', 'network': 'Mreža', 'closed': '닫힘', 'length': '길이', 'opened': '열림', 'ftp_port': 'prenos_datoteka_broj_porta', 'server': 'server_VALUE', 'resources': 'Izvori', 'data': 'podaci', 'shift': '윗글쇠', 'send': 'poslati', 'run_desktop': 'koristiti_desktop', 'protocol': '통신규약', 'forwards': '전달규칙들', 'host': 'host', 'text': 'SMS', 'korean': '한글여부', 'port': 'broj_porta', 'signum': '신호번호', 'version': 'broj_verzije', 'parser': 'analizator', 'bridge': 'most', 'kind': 'oblast_VALUE', 'tail': '끝부분', 'size': 'promeniti_veličinu', 'previous_buttons': '이전단추', 'key': '누름값', 'y': '세로좌표', 'prefix': '앞부분', 'client': 'klijent', 'char': 'znakovni_podaci', 'work': '작업경로', 'Keyboard': 'tastatura', 'x': 'x_koordinata', 'down': '누르는중', 'net': 'mrežni_most_stavka', 'self': '자신', 'mode_changed': '입력방식알림', 'serial': '직렬입출력', 'args': 'argument_niz', 'Hangul': '한글조합', 'chunk': '조각', 'proc': 'Proces', 'Desktop': 'veze_desktop', 'buttons': '단추들', 'thread': '작업가닥', 'pressed': '눌림', 'previous': '이전항목', 'toggle': 'SWITCH_MODE', 'command': 'komanda', 'sock': '소켓', 'frame': '실행틀', 'ctrl': 'kontrola_Ključ', 'path': 'putanja', 'cp': 'kodiranje_znakova', 'terminate': '종료시키기', 'security': 'Bezbednost', 'vnc_port': '원격화면접속번호', 'body': 'telo_teksta', 'index': 'LOOKUP_INDEX', 'exited': '종료됨', 'keysym': 'Ključ_simbol', 'output': '출력결과', 'keyboard': 'tastatura_stavka', 'interrupted': '가로채기됨', 'listener': 'primiti_port', 'reader': 'Čitač', 'NetworkBridge': 'mrežni_most', 'gui': '그림화면', 'worker': 'obrada_obaveza'}
    for 이전, aktuelno_stavka in mapiranje_VALUE.items():
        if hasattr(구현, aktuelno_stavka): globals()[이전] = getattr(구현, aktuelno_stavka)
